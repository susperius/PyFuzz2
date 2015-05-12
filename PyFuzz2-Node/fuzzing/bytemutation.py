__author__ = 'susperius'

import random
import helper
import fuzzer


class ByteMutation(fuzzer.Fuzzer):
    NAME = "bytemutation"
    CONFIG_PARAMS = ["fuzz_file", "min_change", "max_change", "seed", "file_type"]

    def __init__(self, fuzz_file, min_change=1, max_change=1, seed=31337, file_type="png"):
        self._fuzz_file = fuzz_file
        self._data = ""
        self._count = 0
        self.__load_fuzz_file()
        self._seed = seed
        self._min_change = min_change
        self._max_change = max_change
        self._file_type = file_type
        if seed == 0:
            random.seed()
        else:
            random.seed(self._seed)

    def __load_fuzz_file(self):
        with open(self._fuzz_file, "rb") as fd:
            self._data = fd.read()
        self._count = 0

    @property
    def file_type(self):
        return self._file_type

    @property
    def prng_state(self):
        return random.getstate()

    def set_state(self, state):
        random.setstate(state)

    def fuzz(self):
        data_length = len(self._data)
        changes = min(random.randint(self._min_change, self._max_change), data_length)
        for i in range(changes):
            num = random.randint(0, data_length)
            fuzz_byte = random.choice(helper.BYTE_MATRIX)
            self._data = self._data[:num-1] + fuzz_byte + self._data[num+1:]
        self._count += 1
        if self._count > len(self._data) / 2:
            self.__load_fuzz_file()
        return self._data
