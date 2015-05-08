__author__ = 'susperius'

import logging

import gevent
import gevent.monkey
import pickle
import os
import time
from gevent.queue import Queue
# from fuzzer.fuzzers import FUZZERS
from communication.beaconclient import BeaconClient
from communication.nodelistener import Listener
from worker.listenerworker import ListenerWorker
from worker.debuggerworker import DebuggerWorker
from worker.reportworker import ReportWorker
from model.config import ConfigParser



gevent.monkey.patch_all()

CONFIG_FILENAME = "node_config.xml"
pyfuzznode = None


class PyFuzz2Node:
    def __init__(self, logger, config_filename=CONFIG_FILENAME):
        self._logger = logger
        node_config = ConfigParser(config_filename)
        self._node_name = node_config.node_name
        self._node_mode = node_config.node_mode
        if self._node_mode == "net":
            self._beacon_server, self._beacon_port, self._beacon_interval = node_config.beacon_config
            self._report_server, self._report_port = node_config.report_config
            self._tcp_listener_port = node_config.listener_config
        self._fuzzer_type = node_config.fuzzer_type
        self._fuzzer_config = node_config.fuzzer_config
        self._fuzzer = self.__choose_fuzzer()
        if os.path.isfile("fuzz_state.pickle"):  # Load the saved state of the prng
            with open("fuzz_state.pickle", 'r') as fd:
                self._fuzzer.set_state(pickle.load(fd))
            os.remove("fuzz_state.pickle")
        self._reporter_queue = Queue()
        if self._node_mode == "net":
            self._listener_queue = Queue()
            self._beacon_client = BeaconClient(self._beacon_server, self._beacon_port, self._node_name,
                                               self._beacon_interval, self._tcp_listener_port)
            self._tcp_listener = Listener(self._tcp_listener_port, self._listener_queue)
            self._listener_worker = ListenerWorker(self._listener_queue)
            self._report_worker = ReportWorker(True, self._reporter_queue, self._fuzzer.file_type,
                                               node_config.program_path, self._report_server, self._report_port)
        else:
            self._report_worker = ReportWorker(False, self._reporter_queue, self._fuzzer.file_type,
                                               node_config.program_path)
        self._debugger_worker = DebuggerWorker(node_config.program_path, self._fuzzer, self._reporter_queue,
                                               node_config.sleep_time, node_config.dbg_child)

    def __choose_fuzzer(self):
        if self._fuzzer_type == "bytemutation":
            from fuzzer.bytemutation import ByteMutation

            return ByteMutation(self._fuzzer_config[0], self._fuzzer_config[1], self._fuzzer_config[2],
                                self._fuzzer_config[3], self._fuzzer_config[4])
        elif self._fuzzer_type == "js_fuzzer":
            from fuzzer.javascript import JsFuzz

            return JsFuzz(self._fuzzer_config[0], self._fuzzer_config[1],
                          self._fuzzer_config[2], self._fuzzer_config[3], self._fuzzer_config[4])

    def __stop_all_workers(self):
        self._debugger_worker.stop_worker()
        if self._node_mode == "net":
            self._listener_worker.stop_worker()
            self._beacon_client.stop_beacon()

    def __save_fuzz_state(self):
        fuzz_state = self._fuzzer.get_state()
        with open("fuzz_state.pickle", 'w+') as fd:
            pickle.dump(fuzz_state, fd)  # Save the state of the prng

    def main(self):
        start = time.time()
        self._logger.info("PyFuzz 2 Node started ...")
        if self._node_mode == "net":
            self._beacon_client.start_beacon()
            self._tcp_listener.serve()
            self._listener_worker.start_worker()
        self._report_worker.start_worker()
        self._debugger_worker.start_worker()
        while True:
            try:
                if self._node_mode == "net":
                    if self._listener_worker.new_config:
                        self.__stop_all_workers()
                        self.__save_fuzz_state()
                        restart()
                    elif self._listener_worker.reset:
                        self.__stop_all_workers()
                        self.__save_fuzz_state()
                        reboot()
                if time.time() - start > (6*60*60):  # Reboot after six hours
                    self.__stop_all_workers()
                    self.__save_fuzz_state()
                    reboot()
                gevent.sleep(0)
            except KeyboardInterrupt:
                self.__stop_all_workers()
                quit()


def reboot():
    import subprocess
    subprocess.call("shutdown /f /r /t 5")


def restart():
    pyfuzznode = PyFuzz2Node(logger)
    pyfuzznode.main()


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
if __name__ == "__main__":
    pyfuzznode = PyFuzz2Node(logger)
    pyfuzznode.main()