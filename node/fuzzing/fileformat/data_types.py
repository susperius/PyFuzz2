__author__ = 'susperius'

import os
import random
from ..browser.jsfuzzer.values import FuzzValues


class DataTypes:
    def __init__(self, seed):
        self._DATA_TYPES = {'SHORT': (self.__get_random_bytes, 2),
                             'INT': (self.__get_random_bytes, 4),
                             'STRING_ASCII': (self.__get_random_string_ascii, 1),
                             'STRING_UNICODE': (self.__get_random_bytes, 1),
                             'CHAR': (self.__get_char, None)}
        self._random = random.random()
        self._random.seed(seed)

    def get_random_data(self, data_type, length):
        if data_type not in self._DATA_TYPES.keys():
            return None
        else:
            return self._DATA_TYPES[data_type][0](length/self._DATA_TYPES[data_type][1]) if self._DATA_TYPES[data_type][1] is not None else self._DATA_TYPES[data_type][0]()

    def __get_random_bytes(self, length):
        ret_val = "" + os.urandom(length)
        return ret_val

    def __get_random_string_ascii(self, length):
        ret_val = ""
        for i in range(length):
            ret_val += self._random.choice(FuzzValues.CHARS)
        return ret_val

    def __get_char(self):
        return self._random.choice(FuzzValues.CHARS)
