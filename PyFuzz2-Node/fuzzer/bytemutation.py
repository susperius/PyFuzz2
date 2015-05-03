__author__ = 'susperius'

import random
import helper

NAME = "bytemutation"
CONFIG_PARAMS = ["fuzz_file", "min_change", "max_change", "seed", "file_type"]


class ByteMutation:
    def __init__(self, fuzz_file, min_change=1, max_change=1, seed=31337, file_type="png"):
        self._seed = seed
        self._min_change = min_change
        self._max_change = max_change
        self._file_type = file_type
        random.seed(self._seed)

    @property
    def file_type(self):
        return self._file_type

    @property
    def get_state(self):
        return random.getstate()

    def set_state(self, state):
        random.setstate(state)

    def fuzz(self, input_data):
        data = input_data
        data_length = len(data)
        changes = min(random.randint(self._min_change, self._max_change), data_length)
        for i in range(changes):
            num = random.randint(0, data_length)
            fuzz_byte = random.choice(helper.BYTE_MATRIX)
            data = data[:num-1] + fuzz_byte + data[num+1:]
        return data
