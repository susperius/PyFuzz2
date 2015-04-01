__author__ = 'susperius'

import logging
import gevent
import gevent.monkey
import xml.etree.ElementTree as ET

from communication.beaconclient import BeaconClient
from communication.tcplistener import Listener
from gevent.queue import Queue
from fuzzer.fuzzers import FUZZERS

gevent.monkey.patch_all()

CONFIG_FILENAME = "node_config.xml"


class PyFuzz2Node:
    def __init__(self, logger, config_filename=CONFIG_FILENAME):
        self._logger = logger
        self._node_name = ""
        self._beacon_server = ""
        self._beacon_port = 0
        self._beacon_interval = 0
        self._tcp_listener_port = 0
        self._fuzzer = None
        self._fuzz_file = ""
        self._read_config(config_filename)
        self._task_queue = Queue()
        self._beacon_client = BeaconClient(self._beacon_server, self._beacon_port, self._node_name,
                                           self._beacon_interval, self._tcp_listener_port)
        self._tcp_listener = Listener(self._tcp_listener_port, self._task_queue)

    def _read_config(self, config_filename):
        tree = ET.parse(config_filename)
        root = tree.getroot()
        beacon = root.find("beacon")
        listener = root.find("listener")
        fuzzer_conf = root.find("fuzzer")
        self._node_name = root.attrib['name']
        self._beacon_server = beacon.attrib['server']
        self._beacon_port = int(beacon.attrib['port'])
        self._beacon_interval = int(beacon.attrib['interval'])
        self._tcp_listener_port = int(listener.attrib['port'])
        self._fuzzer = self._choose_fuzzer(fuzzer_conf)


    def _choose_fuzzer(self, fuzzer_conf):
        f_type = fuzzer_conf.attrib['type']
        if f_type in FUZZERS:
            if f_type == "bytemutation":
                from fuzzer.bytemutation import ByteMutation
                min_change = int(fuzzer_conf.attrib['min_change'])
                max_change = int(fuzzer_conf.attrib['max_change'])
                seed = int(fuzzer_conf.attrib['seed'])
                iteration = int(fuzzer_conf.attrib['iteration'])
                self._fuzz_file = fuzzer_conf.attrib['fuzz_file']
                return ByteMutation(min_change, max_change, seed, iteration)
        else:
            raise Exception("No such fuzzer!")
        pass


    def main(self):
        self._logger.info("PyFuzz 2 Node started ...")
        self._beacon_client.start_beacon()
        self._tcp_listener.serve()
        while True:
            try:
                if not self._task_queue.empty():
                    task = self._task_queue.get_nowait()
                    self._logger.debug(task)
                gevent.sleep(0)
            except KeyboardInterrupt:
                quit()


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    pyfuzznode = PyFuzz2Node(logger)
    pyfuzznode.main()