__author__ = 'susperius'

import time
import gevent
import gevent.monkey
import pickle
from gevent import socket

#gevent.monkey.patch_all()

class BeaconClient():
    def __init__(self, beacon_server, beacon_port, node_name, beacon_interval=10, tcp_listener_port=31337):
        self._beacon_server = beacon_server
        self._beacon_port = beacon_port
        self._node_name = node_name
        self._beacon_running = False
        self._beacon_greenlet = None
        self._beacon_interval = beacon_interval
        self._tcp_listener_port = tcp_listener_port

    def __beacon(self):
        while True:
            sock_fd = socket.socket(type=socket.SOCK_DGRAM)
            beacon_data = [0x01, [self._node_name, self._tcp_listener_port]]
            sock_fd.sendto(pickle.dumps(beacon_data), (self._beacon_server, self._beacon_port))
            sock_fd.close()
            gevent.sleep(self._beacon_interval)
        pass

    def start_beacon(self):
        if not self._beacon_running:
            self._beacon_greenlet = gevent.spawn(self.__beacon)
            self._beacon_running = True

    # TODO: implement stop_beacon
    def stop_beacon(self):
        pass