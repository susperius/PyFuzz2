__author__ = 'susperius'

import random
import helper


class ByteMutation:
    def __init__(self, min_change=1, max_change=1, seed=None, iteration=0):
        self._seed = seed
        self._min_change = min_change
        self._max_change = max_change
        self._iteration = iteration
        random.seed(self._seed)
        if self._iteration != 0: # Set the old state for iteration x
            for i in range(self._iteration):
                random.randint(1, 10)

    @property
    def config_attribs(self):
        return ['min_change', 'max_change', 'seed', 'iteration'] #same order as in the __init__

    @property
    def name(self):
        return "bytemutation"

    def fuzz(self, input_data):
        data = input_data
        data_length = len(data)
        changes = min(random.randint(self._min_change, self._max_change), data_length)
        for i in range(changes):
            num = random.randint(0, data_length)
            fuzz_byte = random.choice(helper.BYTE_MATRIX)
            data = data[:num-1] + fuzz_byte + data[num+1:]
        return data
