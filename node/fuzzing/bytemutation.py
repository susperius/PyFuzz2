import random

import helper
import fuzzer


class ByteMutation(fuzzer.Fuzzer):
    NAME = "bytemutation"
    CONFIG_PARAMS = ["fuzz_file", "min_change", "max_change", "file_type"]

    def __init__(self, fuzz_file, min_change=1, max_change=1, file_type="png"):
        self._fuzz_file = fuzz_file
        self._data = ""
        self._count = 0
        self.__load_fuzz_file()
        self._seed = int(seed)
        self._min_change = int(min_change)
        self._max_change = int(max_change)
        self._file_type = file_type

    @classmethod
    def from_list(cls, params):
        return cls(params[0], params[1], params[2], params[3], params[4])

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

    def set_seed(self, seed=0):
        random.seed(seed)

    def create_testcases(self, count, directory):
        self.clear_folder(directory)
        for i in range(count):
            file_name = "test_0" + str(i) + "." + self.file_type if i < 10 else "test_" + str(i) + "." + self.file_type
            with open(directory + "/" + file_name, 'wb+') as fd:
                fd.write(self.fuzz())

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
