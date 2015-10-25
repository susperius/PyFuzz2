__author__ = 'susperius'

from ..fuzzer import Fuzzer


class FileFormatFuzzer(Fuzzer):
    NAME = "file_format_fuzzer"
    CONFIG_PARAMS = ["config_file"]

    def __init__(self, programs, config_file):

        pass

    def fuzz(self):
        pass

    @classmethod
    def from_list(cls, params):
        pass

    def prng_state(self):
        pass

    def create_testcases(self, count, directory):
        pass

    def file_type(self):
        pass

    def set_seed(self, seed):
        pass

    def set_state(self, state):
        pass

