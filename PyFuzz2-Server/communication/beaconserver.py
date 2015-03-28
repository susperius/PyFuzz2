__author__ = 'susperius'

import logging
import gevent
import gevent.monkey

from gevent.server import DatagramServer
from model.task import Task


gevent.monkey.patch_all()


class BeaconServer:
    def __init__(self, port, task_queue):
        self._port = port
        self._serving = False
        self._serving_greenlet = None
        self._beacon_server = None
        self._logger = logging.getLogger(__name__)
        self._task_queue = task_queue

    def __serve(self):
        self._logger.info("[Beacon Server] initialized on port " + str(self._port) + " ...")
        self._beacon_server = DatagramServer(('', self._port), self.__beacon_receiver)
        self._beacon_server.serve_forever()

    def __beacon_receiver(self, msg, address):
        if ord(msg[0]) == 0x01:
            self._task_queue.put(Task(0x01, address[0], msg[1:]))

    def serve(self):
        if not self._serving:
            self._serving_greenlet = gevent.spawn(self.__serve)
            self._serving = True
            gevent.sleep(0)
        else:
            pass
