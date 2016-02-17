__author__ = 'susperius'
#  TODO: Make it pretty and functional as fuzzer
import random

from ..fuzzer import Fuzzer
from model.values import FuzzValues
from model.CssProperties import CSS_STYLES


class CssFuzzer(Fuzzer):
    NAME = "CssFuzzer"
    CONFIG_PARAMS = ["seed"]

    def __init__(self, seed="0"):
        self._tags = []
        self._class_names = []
        if int(seed) == 0:
            random.seed()
        else:
            random.seed(int(seed))

    def set_tags(self, tags):
        self._tags = tags

    def set_class_names(self, class_names):
        self._class_names = class_names

    def set_options(self, tags, class_names):
        self._tags = tags
        self._class_names = class_names

    def prng_state(self):
        return random.getstate()

    def set_state(self, state):
        random.setstate(state)

    @classmethod
    def from_list(cls, params):
        pass

    def create_testcases(self, count, directory):
        pass

    def fuzz(self):
        style = ""
        for tag in self._tags:
            style += self.__create_style(tag)
        for class_name in self._class_names:
            style += self.__create_style("." + class_name)
        return style

    def __create_style(self, css_selector):
        style = css_selector + "{\n"
        for i in range(random.randint(5,100)):
            style += "\t" + self.__create_style_statement() + "\n"
        style += "}\n"
        return style

    def __create_style_statement(self):
        prop = random.choice(CSS_STYLES)
        val = random.choice(prop[1:])
        return prop[0] + " : " + val + ";"

    def set_seed(self, seed):
        random.seed(int(seed))

    def file_type(self):
        return "css"
