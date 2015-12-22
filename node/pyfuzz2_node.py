__author__ = 'susperius'

import logging

import gevent
import gevent.monkey
import pickle
import os
import time
from gevent.queue import Queue
# from fuzzing.fuzzers import FUZZERS
from communication.beaconclient import BeaconClient
from communication.nodelistener import Listener
from worker.listenerworker import ListenerWorker
from worker.fuzzingworker import FuzzingWorker
from worker.reducingworker import ReducingWorker
from worker.reportworker import ReportWorker
from model.config import ConfigParser
from fuzzing.fuzzers import FUZZERS
from reducing.reducers import REDUCERS


gevent.monkey.patch_all()

CONFIG_FILENAME = "node_config.xml"
pyfuzznode = None


class PyFuzz2Node:
    def __init__(self, logger, config_filename=CONFIG_FILENAME):
        self._logger = logger
        self._node_config = ConfigParser(config_filename)
        self._reporter_queue = Queue()
        if self._node_config.node_net_mode == "net":
            beacon_server, beacon_port, beacon_interval = self._node_config.beacon_config
            report_server, report_port = self._node_config.report_config
            tcp_listener_port = self._node_config.listener_config
            self._listener_queue = Queue()
            self._beacon_client = BeaconClient(beacon_server, beacon_port, self._node_config.node_name,
                                               beacon_interval, tcp_listener_port)
            self._tcp_listener = Listener(tcp_listener_port, self._listener_queue)
            self._listener_worker = ListenerWorker(self._listener_queue, self._reporter_queue)
            self._report_worker = ReportWorker(True, self._reporter_queue, self._node_config.file_type,
                                               self._node_config.programs, report_server, report_port)
        else:  # else single mode
            self._report_worker = ReportWorker(False, self._reporter_queue, self._node_config.file_type,
                                               self._node_config.programs)
        if self._node_config.node_op_mode == 'fuzzing':
            self._fuzzer = self.__choose_fuzzer()
            if os.path.isfile("fuzz_state.pickle"):
                try:
                    with open("fuzz_state.pickle", 'r') as fd:
                        self._fuzzer.set_state(pickle.load(fd))
                    os.remove("fuzz_state.pickle")
                except KeyError as er:
                    self._logger.error("Error while restoring the PRNG state -> " + er.message)
                    self._fuzzer.set_seed()
            self._operation_worker = FuzzingWorker(self._node_config.programs, self._fuzzer, self._reporter_queue,)
        elif self._node_config.node_op_mode == 'reducing':
            self._reducer = self.__choose_reducer()
            self._operation_worker = ReducingWorker(self._reducer, self._node_config.programs, self._reporter_queue)
        else:
            raise ValueError('Unsupported operation mode!')

    def __choose_fuzzer(self):
        return FUZZERS[self._node_config.fuzzer_type][1].from_list(self._node_config.fuzzer_config)

    def __choose_reducer(self):
        return REDUCERS[self._node_config.reducer_type][1].from_list(self._node_config.reducer_config)

    def __stop_all_workers(self):
        self._operation_worker.stop_worker()
        if self._node_config.node_net_mode == "net":
            self._listener_worker.stop_worker()
            self._beacon_client.stop_beacon()
            self._tcp_listener.stop()

    def __save_fuzz_state(self):
        fuzz_state = self._fuzzer.prng_state
        with open("fuzz_state.pickle", 'w+') as fd:
            pickle.dump(fuzz_state, fd)  # Save the state of the prng

    def main(self):
        start = time.time()
        self._logger.info("PyFuzz 2 Node started ...")
        if self._node_config.node_net_mode == "net":
            self._beacon_client.start_beacon()
            self._tcp_listener.serve()
            self._listener_worker.start_worker()
        self._report_worker.start_worker()
        self._operation_worker.start_worker()
        while True:
            try:
                if self._node_config.node_net_mode == "net":
                    if self._listener_worker.new_config:
                        self._logger.info("Received new config")
                        self.__stop_all_workers()
                        # self.__save_fuzz_state() if there is a new config it shouldn't restore the state??
                        restart(self._node_config.sleep_time + 5)
                    elif self._listener_worker.reset:
                        self._logger.info("Node is going to reboot on received command")
                        self.__stop_all_workers()
                        gevent.sleep(5)
                        if self._node_config.node_op_mode == "fuzzing":
                            self.__save_fuzz_state()
                        gevent.sleep(self._node_config.sleep_time + 5)
                        reboot()
                if time.time() - start > self._node_config.reboot_time:  # Reboot after eight hours
                    self._logger.info("Node is going to reboot")
                    self.__stop_all_workers()
                    gevent.sleep(5)
                    if self._node_config.node_op_mode == "fuzzing":
                        self.__save_fuzz_state()
                    gevent.sleep(self._node_config.sleep_time + 5)
                    reboot()
                gevent.sleep(5)  # It's enough to check the above stuff every 5 seconds instead of burning cpu time
            except KeyboardInterrupt:
                self.__stop_all_workers()
                quit()


def reboot():
    import subprocess
    subprocess.call("shutdown /f /r /t 5")


def restart(wait_time):
    gevent.sleep(wait_time)
    os.system("python pyfuzz2_node.py ")

formatter = logging.Formatter("%(levelname)s: %(message)s")
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("log/node.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
if __name__ == "__main__":
    pyfuzznode = PyFuzz2Node(logger)
    pyfuzznode.main()
