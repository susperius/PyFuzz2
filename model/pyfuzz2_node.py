import time


class PyFuzz2Node:
    def __init__(self, name, address, listener_port):
        self._name = name
        self._address = address
        self._listener_port = listener_port
        self._is_active = True
        self._last_beacon = time.time()
        self._crashes = {}
        self._config = None

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
        return {"status": "Active" if self.status else "Inactive",
                "crashes": str(self.crashes),
                "last_contact": self.last_contact,
                "addr": self.address,
                "name": self.name}

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

    @status.setter
    def status(self, is_active):
        self._is_active = is_active

    @property
    def last_contact(self):
        return time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(self._last_beacon))

    @property
    def crashes(self):
        return len(self._crashes.keys())

    @property
    def crash_hashes(self):
        return self._crashes.keys()

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config

    def crashed(self, major_hash):
        if major_hash in self._crashes.keys():
            self._crashes[major_hash] += 1
        else:
            self._crashes[major_hash] = 1

    def dump(self):
        return "Name: " + self._name + " Status: " + str(self._is_active) + " Last contact: " + time.strftime(
            "%a, %d %b %Y %H:%M:%S", time.localtime(self._last_beacon))