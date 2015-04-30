__author__ = 'susperius'

import logging

import gevent
import gevent.monkey
from gevent.queue import Queue
from fuzzer.fuzzers import FUZZERS
from communication.beaconclient import BeaconClient
from communication.tcplistener import Listener
from worker.listenerworker import ListenerWorker
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
        self._listener_queue = Queue()
        self._beacon_client = BeaconClient(self._beacon_server, self._beacon_port, self._node_name,
                                           self._beacon_interval, self._tcp_listener_port)
        self._tcp_listener = Listener(self._tcp_listener_port, self._listener_queue)
        self._listener_worker = ListenerWorker(self._listener_queue)

    def __choose_fuzzer(self):
        if self._fuzzer_type == "bytemutation":
            from fuzzer.bytemutation import ByteMutation
            return ByteMutation(self._fuzzer_config[0], self._fuzzer_config[1], self._fuzzer_config[2],
                                        self._fuzzer_config[3], self._fuzzer_config[4])
        elif self._fuzzer_type == "js_fuzzer":
            from fuzzer.javascript import JsFuzz
            return JsFuzz(self._fuzzer_config[0], self._fuzzer_config[1],
                          self._fuzzer_config[2], self._fuzzer_config[3])

    def main(self):
        self._logger.info("PyFuzz 2 Node started ...")
        self._beacon_client.start_beacon()
        self._tcp_listener.serve()
        self._listener_worker.start_worker()
        while True:
            try:
                if self._listener_worker.new_config:
                    restart()
                gevent.sleep(0)
            except KeyboardInterrupt:
                quit()


def restart():
    pyfuzznode = PyFuzz2Node(logger)
    pyfuzznode.main()

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
if __name__ == "__main__":
    pyfuzznode = PyFuzz2Node(logger)
    pyfuzznode.main()