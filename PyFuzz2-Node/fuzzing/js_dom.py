__author__ = 'susperius'

from jsfuzzer.JsDocument import *
from jsfuzzer.JsElement import *
from jsfuzzer.JsAttrNodeMap import *
from jsfuzzer.JsGlobal import JsGlobal
from jsfuzzer.domObjects import *
from jsfuzzer.htmlObjects import *
from jsfuzzer.values import *
from html import HtmlFuzzer
import fuzzer
import random
import os

TEMPLATE_FILE = "fuzzing/jsfuzzer/template.dat"

NL = "\n"

class JsDomFuzzer(fuzzer.Fuzzer):
    def __init__(self):
        pass

    def fuzz(self):
        pass

    @property
    def prng_state(self):
        return random.getstate()

    @property
    def file_type(self):
        pass

    def set_state(self, state):
        random.setstate(state)