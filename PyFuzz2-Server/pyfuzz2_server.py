__author__ = 'susperius'

import logging
import gevent
import gevent.monkey

from model.task import Task
from model.message_types import MESSAGE_TYPES
from model.node import PyFuzz2Node
from gevent.queue import Queue
from communication.beaconserver import BeaconServer
from communication.reportserver import ReportServer
from communication.tcpclient import TcpClient
from beacon.beaconworker import BeaconWorker

gevent.monkey.patch_all()

#TODO: 3) Nodes' TCP Listener for incoming settings and other stuff


class PyFuzz2Server:
    def __init__(self, logger):
        self._logger = logger
        self._logger.info("PyFuzz2 Server started...")
        self._beacon_queue = Queue()
        self._beacon_server = BeaconServer(31337, self._beacon_queue)
        self._beacon_worker = BeaconWorker(self._beacon_queue)
        self._report_queue = Queue()
        self._report_server = ReportServer(31338, self._report_queue)
        self._report_server.serve()
        self._node_dict = {}

    def main(self):
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