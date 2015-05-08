__author__ = 'susperius'

import gevent
import logging

from gevent.queue import Queue
from model.task import Task
from model.node import PyFuzz2Node


class BeaconWorker:
    def __init__(self, beacon_queue, timeout):
        self._beacon_queue = beacon_queue
        self._logger = logging.getLogger(__name__)
        self._active = False
        self._node_dict = {}
        self._timeout = timeout
        self._greenlets = []

    def __beacon_worker_green(self):
        while True:
            if not self._beacon_queue.empty():
                    actual_task = self._beacon_queue.get_nowait()
                    self.__beacon_worker(actual_task)
            gevent.sleep(0)

    def __beacon_worker(self, task):
        beacon = (task.get_task()['sender'], task.get_task()['msg'].split(':')[0], task.get_task()['msg'].split(':')[1])
        if not beacon[0] in self._node_dict:
            self._node_dict[beacon[0]] = PyFuzz2Node(beacon[1], beacon[0], beacon[2])
        else:
            self._node_dict[beacon[0]].beacon_received()
            self._node_dict[beacon[0]].address = beacon[0]
        self._logger.debug(self._node_dict[beacon[0]].dump())

    def __check_all_beacons(self):
        while True:
            for key, node in self._node_dict.items():
                if not node.check_status() and not node.check_status(self._timeout):
                    self._logger.debug("Node: " + node.name + " is inactive")
            gevent.sleep(40)

    @property
    def nodes(self):
        return self._node_dict

    def start_worker(self):
        if not self._active:
            self._greenlets.append(gevent.spawn(self.__beacon_worker_green))
            self._greenlets.append(gevent.spawn(self.__check_all_beacons))
            self._active = True
            gevent.sleep(0)

    def stop_worker(self):
        if self._active:
            gevent.killall(self._greenlets)
            self._active = False