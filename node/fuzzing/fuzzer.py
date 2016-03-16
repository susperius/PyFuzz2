import os

__author__ = 'susperius'

"""
Abstract class used to implement own fuzzers
"""


class Fuzzer:
    NAME = []
    CONFIG_PARAMS = []

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

    @staticmethod
    def clear_folder(folder):
        for file_name in os.listdir(folder):
            if "py" in file_name:
                continue
            file_path = os.path.join(folder, file_name)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                print e
