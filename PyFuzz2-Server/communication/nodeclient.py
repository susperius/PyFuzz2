__author__ = 'susperius'


import gevent
import gevent.monkey
import gevent.socket
from gevent import socket

#gevent.monkey.patch_all()


class NodeClient():
    def __init__(self, node_listener, node_port):
        self._node_listener = node_listener
        self._node_port = node_port

    def send_to_node(self, data):
        sock = gevent.socket.create_connection((self._node_listener, self._node_port))
        sock.send(data)
        sock.close()
