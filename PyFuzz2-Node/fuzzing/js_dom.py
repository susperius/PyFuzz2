__author__ = 'susperius'

from jsfuzzer.JsDocument import *
from jsfuzzer.JsElement import *
from jsfuzzer.JsAttrNodeMap import *
from jsfuzzer.JsGlobal import JsGlobal
from jsfuzzer.domObjects import *
from jsfuzzer.htmlObjects import *
from jsfuzzer.values import *
from jsfuzzer.browserObjects import *
from html import HtmlFuzzer
import fuzzer
import random
import os

TEMPLATE_FILE = "fuzzing/jsfuzzer/template.dat"

class JsDomFuzzer(fuzzer.Fuzzer):
    NAME = "js_dom_fuzzer"
    CONFIG_PARAMS = ["starting_element", "total_operations", "browser", "seed", "file_type"]

    def __init__(self, starting_elements, total_operations, browser, seed=31337, file_type='html'):
        self._starting_elements = starting_elements
        self._total_operations = total_operations
        self._browser = browser
        self._html_fuzzer = HtmlFuzzer(self._starting_elements, 3, seed)
        random.seed(seed)
        self._file_type = file_type
        self._function_count = 0
        self._operations_count = 0
        self._js_elements = {}
        """:type dict(JsElement)"""
        self._window_timeout = 40

    @property
    def prng_state(self):
        return random.getstate()

    @property
    def file_type(self):
        return self._file_type

    @staticmethod
    def __get_html_ids(html):
        start = html.find("IDS:") + 5
        end = html.find("-->")
        ids = html[start:end].split("; ")
        del(ids[-1])
        return ids

    def fuzz(self):
        self._function_count = 0
        self._operations_count = 0
        html = self._html_fuzzer.fuzz()
        ids = self.__get_html_ids(html)
        js_code = self.__create_startup(ids)
        while self._total_operations > self._operations_count:
            js_code += self.__create_function()
        js_code = js_code.replace(Window.setTimeout("func" + str(self._function_count) + "()", self._window_timeout), "//end")
        return js_code

    def set_state(self, state):
        random.setstate(state)

    def __create_startup(self, elem_ids):
        code = "function startup() {\n"
        i = 0
        for elem_id in elem_ids:
            code += "\t" + "elem" + str(i) + " = " + JsDocument.getElementById(elem_id) + "\n"
            self._js_elements["elem"+str(i)] = JsElement("elem"+str(i))
        code += "\t" + Window.setTimeout("func0"+"()", self._window_timeout) + "\n}\n"
        return code

    def __create_function(self):
        code = "function func" + str(self._function_count) + "() {\n"
        func_count = random.randint(10, 50)
        for i in range(func_count):
            code += "\t" + self.__create_element_method() + "\n"
        self._function_count += 1
        code += "\t" + Window.setTimeout("func" + str(self._function_count) + "()", self._window_timeout) + " \n}\n"
        return code

    def __create_element_method(self):
        code = ""
        key = random.choice(self._js_elements.keys())
        method = random.choice(DomObjects.DOM_ELEMENT_METHODS)
        if method == 'addEventListener':
            code += self._js_elements[key].addEventListener(random.choice(DomObjects.DOM_EVENTS))
        elif method == 'appendChild':
            if random.randint(1, 100) < 80:
                code += self._js_elements[key].appendChild(self._js_elements[random.choice(self._js_elements.keys())])
            else:
                code += "elem_cr" + str(len(self._js_elements)) + " = " + JsDocument.createElement(random.choice(HtmlObjects.HTML_OBJECTS))
                self._js_elements["elem_cr" + str(len(self._js_elements))] = JsElement("elem_cr" + str(len(self._js_elements)))
                code += self._js_elements[key].appendChild("elem_cr" + str(len(self._js_elements)))
        elif method == 'cloneNode':
            code += "elem_cr" + str(len(self._js_elements)) + " = " + self._js_elements[key].cloneNode(True)
            self._js_elements["elem_cr" + str(len(self._js_elements))] = JsElement("elem_cr" + str(len(self._js_elements)))
            self._js_elements["elem_cr" + str(len(self._js_elements))].children = self._js_elements[key].children
        elif method == 'hasAttribute':
            code += self._js_elements[key].hasAttribute(random.choice(HtmlObjects.HTML_ATTR_GENERIC))
        elif method == 'hasChildNode':
            code += self._js_elements[key].hasChildNodes()
        elif method == 'insertBefore':
            if self._js_elements[key].children is not []:
                code += self._js_elements[key]
        elif method == 'normalize':
            code += self._js_elements[key]
        elif method == 'removeAttribute':
            code += self._js_elements[key]
        elif method == 'removeChild':
            code += self._js_elements[key]
        elif method == 'replaceChild':
            code += self._js_elements[key]
        elif method == 'removeEventListener':
            code += self._js_elements[key]
        elif method == 'setAttribute':
            code += self._js_elements[key]
        elif method ==  'REPLACE_EXIST_ELEMENT':
            code += self._js_elements[key]
        elif method == 'MIX_REFERENCES':
            code += self._js_elements[key]
        self._operations_count += 1
        return code
