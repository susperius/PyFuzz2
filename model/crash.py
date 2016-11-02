__author__ = 'susperius'


class Crash:
    FIELDS = ["Program", "Major Hash", "Minor Hash", "Short Description", "Classification", "Nodes", "Count"]

    def __init__(self, node_address, program, maj_hash, min_hash, short_description, classification,
                 count=1):
        self._node_addresses = set()
        if type(node_address) is not set:
            self._node_addresses = set()
            self.node_addresses.add(node_address)
        else:
            self._node_addresses = self._node_addresses.union(node_address)
        self._program = program
        self._maj_hash = maj_hash
        self._min_hash = min_hash
        self._short_descr = short_description
        self._classification = classification
        self._count = count

    def add_node_address(self, node_address):
        self._node_addresses.add(node_address)
        self._count += 1

    @property
    def node_addresses(self):
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

    @property
    def program(self):
        return self._program

    @property
    def stats(self):
        return { 'maj_hash': self.major_hash, 'min_hash': self.minor_hash,
                'descr': self.short_description, 'nodes': len(self.node_addresses), 'classification': self.classification}