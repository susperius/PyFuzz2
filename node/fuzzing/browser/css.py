__author__ = 'susperius'
#  TODO: Make it pretty and functional as fuzzer
import random

from ..fuzzer import Fuzzer
from jsfuzzer.values import FuzzValues


class CssFuzzer(Fuzzer):
    NAME = "CssFuzzer"
    CONFIG_PARAMS = ["seed"]

    def __init__(self, seed="0"):
        self._tags = []
        if int(seed) == 0:
            random.seed()
        else:
            random.seed(int(seed))

    def set_tags(self, tags):
        self._tags = tags

    def prng_state(self):
        return random.getstate()

    def set_state(self, state):
        random.setstate(state)

    @classmethod
    def from_list(cls, params):
        pass

    def fuzz(self):
        style = ""
        for tag in self._tags:
            style += tag + "{\r\n"
            for i in range(random.randint(1, 20)):
                style += "\t" + self.__get_style() + "\r\n"
            style += "}\r\n"
        return style

    def __get_style(self):
        prop = random.choice(FuzzValues.CSS_STYLES)
        val = random.choice(prop)
        return prop[0] + " : " + val + ";"

    def set_seed(self, seed):
        random.seed(int(seed))

    def file_type(self):
        return "css"
