__author__ = 'susperius'

import gevent
import gevent.monkey
from gevent import socket

#gevent.monkey.patch_all()

class BeaconClient():
    def __init__(self, beacon_server, beacon_port, node_name, beacon_timeout=10, tcp_listener_port=31337):
        self.beacon_server = beacon_server
        self.beacon_port = beacon_port
        self.node_name = node_name
        self.beacon_running = False
        self.beacon_greenlet = None
        self.beacon_timeout = beacon_timeout
        self.tcp_listener_port = tcp_listener_port

    def __beacon(self):
        while True:
            sock_fd = socket.socket(type=socket.SOCK_DGRAM)
            sock_fd.sendto("\x01" + self.node_name + ":" + str(self.tcp_listener_port), (self.beacon_server, self.beacon_port))
            sock_fd.close()
            gevent.sleep(self.beacon_timeout)
        pass

    def start_beacon(self):
        if not self.beacon_running:
            self.beacon_greenlet = gevent.spawn(self.__beacon)
            self.beacon_running = True