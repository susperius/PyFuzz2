__author__ = 'susperius'

import random
import helper


def fuzz(input_data, min_change, max_change, seed=None):
    random.seed(seed)
    data = input_data
    data_length = len(data)
    changes = min(random.randint(min_change, max_change), data_length)
    for i in range(changes):
        num = random.randint(0, data_length)
        fuzz_byte = random.choice(helper.BYTE_MATRIX)
        data = data[:num-1] + fuzz_byte + data[num+1:]
    return data
