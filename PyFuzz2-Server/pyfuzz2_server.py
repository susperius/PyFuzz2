__author__ = 'susperius'

import logging

import gevent
import gevent.monkey
import xml.etree.ElementTree as ET
from gevent.queue import Queue
from communication.beaconserver import BeaconServer
from communication.reportserver import ReportServer
from worker.beaconworker import BeaconWorker

gevent.monkey.patch_all()

CONFIG_FILENAME = "server_config.xml"


class PyFuzz2Server:
    def __init__(self, logger, config_filename=CONFIG_FILENAME):
        self._logger = logger
        self._beacon_port = 0
        self._report_port = 0
        self._beacon_timeout = -1
        self.__read_config(config_filename)
        self._beacon_queue = Queue()
        self._beacon_server = BeaconServer(self._beacon_port, self._beacon_queue)
        self._beacon_worker = BeaconWorker(self._beacon_queue, self._beacon_timeout)
        self._report_queue = Queue()
        self._report_server = ReportServer(self._report_port, self._report_queue)
        self._node_dict = {}

    def __read_config(self, config_filename):
        tree = ET.parse(config_filename)
        root = tree.getroot()
        beacon = root.find("beacon")
        report = root.find("reportServer")
        self._beacon_port = int(beacon.find("server").attrib['port'])
        self._beacon_timeout = int(beacon.find("worker").attrib['timeout'])
        self._report_port = int(report.attrib['port'])

    def main(self):
        self._logger.info("PyFuzz2 Server started...")
        self._beacon_server.serve()
        self._beacon_worker.start_worker()
        self._report_server.serve()
        while True:
            try:
                gevent.sleep(0)
            except KeyboardInterrupt:
                exit(0)

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    server = PyFuzz2Server(logger)
    server.main()