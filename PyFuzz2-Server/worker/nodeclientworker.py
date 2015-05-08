__author__ = 'susperius'

import gevent
import logging
from communication.nodeclient import NodeClient
from worker import Worker


class NodeClientWorker(Worker):
    def __init__(self, working_queue):
        self._logger = logging.getLogger(__name__)
        self._greenlet = None
        self._queue = working_queue
        pass

    def __worker_green(self):
        pass

    def start_worker(self):
        if self._greenlet is not None:
            self._greenlet = gevent.spawn(self.__worker_green)


    def stop_worker(self):
        if self._greenlet is None:
            gevent.kill(self._greenlet)