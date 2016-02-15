import random

from html5 import Html5Fuzzer
from canvas import CanvasFuzzer
from css import CssFuzzer
from ..fuzzer import Fuzzer
from model.JsDocument import JsDocument
from model.JsObject import *

"""
1) Create a html page
2) Fuzz the canvas stuff
3) Create a function to get the DOM elements into variables
4) Fuzz function

FUZZ FUNCTION:



needed methods:
- build a array X
- build if-clause
- build for-loop
- create dom element
- create bool expressions
- create a block (statement_count)
- build statement
"""


class JsFuzzer(Fuzzer):
    NAME = "js_fuzzer"
    CONFIG_PARAMS = []
    CALLING_COMMENT = "//CALLING COMMENT"

    def __init__(self, seed, starting_elements, html_depth, html_max_attr, canvas_size, file_type):
        self._html_fuzzer = Html5Fuzzer(seed, starting_elements, html_depth, html_max_attr, file_type)
        self._canvas_fuzzer = CanvasFuzzer(canvas_size)
        self._css_fuzzer = CssFuzzer(seed)
        random.seed(0)
        self._file_type = file_type
        self._js_objects = []
        self._js_arrays = []

    def file_type(self):
        return self._file_type

    @classmethod
    def from_list(cls, params):
        pass

    def prng_state(self):
        pass

    def set_state(self, state):
        pass

    def create_testcases(self, count, directory):
        pass

    def set_seed(self, seed):
        pass

    def fuzz(self):
        html_page = self._html_fuzzer.fuzz()
        css = self._css_fuzzer.fuzz()
        code = ""

    def __init_js_objects(self, html_page):
        available_dom_elements = html_page.get_elements_by_id()
        code = "function startup() {\n"
        for element_id in available_dom_elements.keys():
            code += "\telem_" + element_id + " = " + JsDocument.getElementById(element_id) + ";\n"
        code += "\t" + self.CALLING_COMMENT + "\n"
        return code

    def __build_js_array(self, length):
        array_obj_list = []
        for i in range(length):
            js_obj = random.choice(self._js_objects)
            array_obj_list.append(js_obj)
        js_array = JsArray("array_" + str(len(self._js_arrays)), array_obj_list)
        self._js_arrays.append(js_array)
        return js_array.newArray()

    def __build_assignment(self):
        pass




