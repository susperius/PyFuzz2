__author__ = 'susperius'

from os import urandom
from random import randint
from random import choice


def mutate_file(in_file, depth):
    operations = ['and', 'or', 'excl_or']
    out_file = in_file
    file_length = len(out_file)
    for i in range(depth):
        op = choice(operations)
        pos = randint(0, file_length - 1)
        mask = ord(bytes(urandom(1)))
        if op == 'and':
            out_file[pos] &= mask
        elif op == 'or':
            out_file[pos] |= mask
        elif op == 'excl_or':
            out_file[pos] ^= mask
    return out_file
