__author__ = 'susperius'


class Crash:
    def __init__(self, node_address, program, maj_hash, min_hash, short_description, classification,
                 node_addresses=None, count=1):
        if node_addresses is None:
            self._node_addresses = set()
            self._node_addresses.add(node_address)
        else:
            self._node_addresses = node_addresses
        self._program = program
        self._maj_hash = maj_hash
        self._min_hash = min_hash
        self._short_descr = short_description
        self._classification = classification
        self._count = count

    def add_node_address(self, node_address):
        self._node_addresses.add(node_address)

    @property
    def node_address(self):
        return self._node_addresses

    @property
    def major_hash(self):
        return self._maj_hash

    @property
    def minor_hash(self):
        return self._min_hash

    @property
    def short_description(self):
        return self._short_descr

    @property
    def classification(self):
        return self._classification

    @property
    def count(self):
        return self._count

