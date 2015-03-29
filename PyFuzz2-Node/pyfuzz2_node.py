__author__ = 'susperius'

import logging
import gevent
import gevent.monkey
import xml.etree.ElementTree as ET

from communication.beaconclient import BeaconClient
from communication.tcplistener import Listener
from gevent.queue import Queue

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
        self._read_config(config_filename)
        self._task_queue = Queue()
        self._beacon_client = BeaconClient(self._beacon_server, self._beacon_port, self._node_name,
                                           self._beacon_interval, self._tcp_listener_port)
        self._tcp_listener = Listener(32337, self._task_queue)
        self._fuzzer = {'type': "", 'options': {}}

    def _read_config(self, config_filename):
        tree = ET.parse(config_filename)
        root = tree.getroot()
        beacon = root.find("beacon")
        listener = root.find("listener")
        self._node_name = root.attrib['name']
        self._beacon_server = beacon.attrib['server']
        self._beacon_port = int(beacon.attrib['port'])
        self._beacon_interval = int(beacon.attrib['interval'])
        self._tcp_listener_port = int(listener.attrib['port'])

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