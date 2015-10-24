__author__ = 'susperius'

import logging
import pickle

import gevent

from communication.nodeclient import NodeClient
from worker import Worker


class NodeClientWorker(Worker):
    def __init__(self, working_queue):
        self._logger = logging.getLogger(__name__)
        self._greenlet = None
        self._queue = working_queue
        pass

    def __worker_green(self):
        while True:
            to_do = self._queue.get()  # [(ip, socket), msg_type, msg])
            address = to_do[0]
            msg_type = to_do[1]
            msg = to_do[2]
            node_client = NodeClient(address[0], address[1])
            node_client.send(pickle.dumps([msg_type, msg], -1))
            gevent.sleep(1)

    def start_worker(self):
        if self._greenlet is None:
            self._greenlet = gevent.spawn(self.__worker_green)
            gevent.sleep(0)

    def stop_worker(self):
        if self._greenlet is not None:
            gevent.kill(self._greenlet)
