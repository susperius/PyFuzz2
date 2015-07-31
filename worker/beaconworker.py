__author__ = 'susperius'

import logging
import pickle

import gevent

from model.node import PyFuzz2Node


class BeaconWorker:
    def __init__(self, beacon_queue, node_worker_queue, timeout):
        self._beacon_queue = beacon_queue
        self._node_worker_queue = node_worker_queue
        self._logger = logging.getLogger(__name__)
        self._active = False
        self._node_dict = {}
        self._timeout = timeout
        self._greenlets = []

    def __beacon_worker_green(self):
        while True:
            actual_task = self._beacon_queue.get()
            self.__beacon_worker(actual_task)
            gevent.sleep(0)

    def __beacon_worker(self, task):  # task = [(ip, port), pickle_data([msg_type, [node_name, listener_port]])]
        data_unpacked = pickle.loads(task[1])
        node_name = data_unpacked[1][0]
        listener_port = data_unpacked[1][1]
        ip, port = task[0]
        if ip not in self._node_dict.keys():
            self._node_dict[ip] = PyFuzz2Node(node_name, ip, listener_port)
            self._node_worker_queue.put([(ip, listener_port), 0x03, ""])  # [(ip, port), GET_CONFIG, ""]
        elif not self._node_dict[ip].status:  # e.g. after a reboot the config also may have changed
            self._node_dict[ip].beacon_received()
            self._node_dict[ip].address = ip
            self._node_dict[ip].name = node_name
            self._node_dict[ip].listener_port = listener_port
            self._node_dict[ip].status = True
            self._node_worker_queue.put([(ip, listener_port), 0x03, ""])  # [(ip, port), GET_CONFIG, ""]
        else:
            self._node_dict[ip].beacon_received()
            self._node_dict[ip].address = ip
        self._logger.debug(self._node_dict[ip].dump())

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