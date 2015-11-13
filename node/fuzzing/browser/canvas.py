from ..fuzzer import Fuzzer

__author__ = 'susperius'

class CanvasFuzzer(Fuzzer):
    NAME = ['canvas_fuzzer']
    CONFIG_PARAMS = []

    def __init__(self):
        pass

    @classmethod
    def from_list(cls, params):
        raise NotImplementedError("ABSTRACT METHOD")

    @property
    def prng_state(self):
        raise NotImplementedError("ABSTRACT METHOD")

    def fuzz(self):
        raise NotImplementedError("ABSTRACT METHOD")

    def set_state(self, state):
        raise NotImplementedError("ABSTRACT METHOD")

    def set_seed(self, seed):
        raise NotImplementedError("ABSTRACT METHOD")

    def create_testcases(self, count, directory):
        raise NotImplementedError("ABSTRACT METHOD")

    @property
    def file_type(self):
        raise NotImplementedError("ABSTRACT METHOD")