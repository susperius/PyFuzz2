__author__ = 'susperius'

import gevent
import gevent.monkey
from gevent import socket

#gevent.monkey.patch_all()

class BeaconClient():
    def __init__(self, beacon_server, beacon_port, beacon_timeout=10, tcp_listener_port=31337):
        self.beacon_server = beacon_server
        self.beacon_port = beacon_port
        self.beacon_running = False
        self.beacon_greenlet = None
        self.beacon_timeout = beacon_timeout
        self.tcp_listener_port = tcp_listener_port

    def __beacon(self):
        while True:
            sock_fd = socket.socket(type=socket.SOCK_DGRAM)
            sock_fd.sendto("\x01" + str(self.tcp_listener_port), (self.beacon_server, self.beacon_port))
            sock_fd.close()
            gevent.sleep(self.beacon_timeout)
        pass

    def start_beacon(self):
        if not self.beacon_running:
            self.beacon_greenlet = gevent.spawn(self.__beacon)

client = BeaconClient("127.0.0.1", 31337)
client.start_beacon()

gevent.sleep(120)