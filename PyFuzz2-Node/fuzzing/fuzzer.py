__author__ = 'susperius'


class Fuzzer:
    @property
    def get_state(self):
        raise NotImplementedError("ABSTRACT METHOD")

    def fuzz(self):
        raise NotImplementedError("ABSTRACT METHOD")

    def set_state(self, state):
        raise NotImplementedError("ABSTRACT METHOD")

    @property
    def file_type(self):
        raise NotImplementedError("ABSTRACT METHOD")