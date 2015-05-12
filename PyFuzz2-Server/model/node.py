__author__ = 'susperius'

import time


class PyFuzz2Node:
    def __init__(self, name, address, listener_port):
        self._name = name
        self._address = address
        self._listener_port = listener_port
        self._is_active = True
        self._last_beacon = time.time()
        self._crashes = 0
        self._config = ""

    def check_status(self, sec=60):
        if time.time() - self._last_beacon > sec:
            self._is_active = False
        else:
            self._is_active = True
        return self._is_active

    def beacon_received(self):
        self._last_beacon = time.time()

    @property
    def info(self):
        return [("Status", "Active" if self.status else "Inactive"),
                ("Crashes", str(self.crashes)),
                ("Last Contact", self.last_contact),
                ("Address", self.address),
                ("Node Name", self.name),
                ("Listener Port", str(self.listener_port))]

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

    @property
    def last_contact(self):
        return time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(self._last_beacon))

    @property
    def crashes(self):
        return self._crashes

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config

    def crashed(self):
        self._crashes += 1

    def dump(self):
        return "Name: " + self._name + " Status: " + str(self._is_active) + " Last contact: " + time.strftime(
            "%a, %d %b %Y %H:%M:%S", time.localtime(self._last_beacon))