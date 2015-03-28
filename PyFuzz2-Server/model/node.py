__author__ = 'susperius'

import time


class PyFuzz2Node:
    def __init__(self, name, address, listener_port):
        self._name = name
        self._address = address
        self._listener_port = listener_port
        self._is_active = True
        self._last_beacon = time.time()

    def check_status(self):
        if time.time() - self._last_beacon > 60:
            self._is_active = False
        else:
            self._is_active = True

    def beacon_received(self):
        self._last_beacon = time.time()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address

    @property
    def listener_port(self):
        return self._listener_port

    @listener_port.setter
    def listener_port(self, port):
        self._listener_port = port

    @property
    def status(self):
        return self._is_active

    def dump(self):
        return "Name: " + self._name + " Status: " + str(self._is_active) + " Last contact: " + time.strftime(
            "%a, %d %b %Y %H:%M:%S", time.localtime(self._last_beacon))