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

gevent.monkey.patch_all()

#TODO: 1) Funtion to see, which nodes called the server CHECK
#TODO: 2) Observe, which node hasn't called home for a specific interval
#TODO: 3) Nodes' TCP Listener for incoming settings and other stuff


class PyFuzz2Server:
    def __init__(self, logger):
        self._logger = logger
        self._logger.info("PyFuzz2 Server started...")
        self._beacon_queue = Queue()
        self._beacon_server = BeaconServer(31337, self._beacon_queue)
        self._beacon_server.serve()
        self._report_queue = Queue()
        self._report_server = ReportServer(31338, self._report_queue)
        self._report_server.serve()
        self._node_dict = {}

    def main(self):
        while True:
            try:
                if not self._beacon_queue.empty():
                    actual_task = self._beacon_queue.get_nowait()
                    self._beacon_worker(actual_task)
                if not self._report_queue.empty():
                    actual_task = self._report_queue.get_nowait()
                    self._report_worker(actual_task)
                gevent.sleep(0)
                pass
            except KeyboardInterrupt:
                exit(0)

    def _beacon_worker(self, task):
        beacon = (task.get_task()['sender'], task.get_task()['msg'].split(':')[0], task.get_task()['msg'].split(':')[0])
        if not beacon[0] in self._node_dict:
            self._node_dict[beacon[0]] = PyFuzz2Node(beacon[1], beacon[0], beacon[2])
        else:
            self._node_dict[beacon[0]].beacon_received()
        logger.debug(self._node_dict[beacon[0]].dump())

    def _report_worker(self, task):
        pass

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    server = PyFuzz2Server(logger)
    server.main()