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
from jsfuzzer.values import FuzzValues
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
        self._occurring_events = {}
        for event in DomObjects.DOM_EVENTS:
            self._occurring_events[event] = 0

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

    def __reinit(self):
        self._function_count = 0
        self._operations_count = 0
        self._function_count = 0
        self._operations_count = 0
        self._js_elements = {}
        """:type dict(JsElement)"""
        self._window_timeout = 40
        self._occurring_events = {}
        for event in DomObjects.DOM_EVENTS:
            self._occurring_events[event] = 0

    def fuzz(self):
        html = self._html_fuzzer.fuzz()
        ids = self.__get_html_ids(html)
        js_code = self.__create_startup(ids)
        while self._total_operations > self._operations_count:
            js_code += self.__add_function()
        js_code = js_code.replace(Window.setTimeout("func" + str(self._function_count) + "()", self._window_timeout),
                                  "event_firing()")
        js_code += self.__add_event_dipatcher()
        js_code += self.__add_event_handlers()
        doc = html.replace("SCRIPT_BODY", js_code)
        self.__reinit()
        return doc

    def set_state(self, state):
        random.setstate(state)

    def __create_startup(self, elem_ids):
        code = "function startup() {\n"
        i = 0
        for elem_id in elem_ids:
            code += "\t" + "elem" + str(i) + " = " + JsDocument.getElementById(elem_id) + "\n"
            self._js_elements["elem"+str(i)] = JsElement("elem"+str(i))
            i += 1
        code += "\t" + Window.setTimeout("func0"+"()", self._window_timeout) + "\n}\n"
        return code

    def __add_function(self, func_name=None, event=False):
        if not func_name:
            func_name = "func" + str(self._function_count) + "()"
        code = "function " + func_name + " {\n"
        func_count = random.randint(10, 50)
        for i in range(func_count):
            code += "\t" + JsGlobal.try_catch_block(self.__add_element_method())
        if not event:
            self._function_count += 1
            code += "\t" + Window.setTimeout("func" + str(self._function_count) + "()", self._window_timeout) + " \n"
        code += "}\n"
        return code

    def __add_event_handlers(self):
        code = ""
        for event in self._occurring_events:
            code += self.__add_function(event + "_handler" + "(event)", True)
        return code

    def __add_event_dipatcher(self):
        code = "function event_firing() {\n"
        for key in self._js_elements:
            for event in self._js_elements[key].registered_events.keys():
                if event == 'click':
                    code += self._js_elements[key].click() + "\n"
                elif event == 'error':
                    pass
                elif event == 'load':
                    pass
                elif event == 'scroll':
                    code += self._js_elements[key].prop_scrollLeft() + " = 10;" + "\n"
                elif event == 'resize' or event == 'change':
                    code += self._js_elements[key].prop_innerHtml() + " = \"" + "A" * 100 + "\";\n"
                elif event == 'focus' or event == 'focusin':
                    code += self._js_elements[key].focus() + "\n"
                elif event == 'blur':
                    code += self._js_elements[key].blur() + "\n"
                elif event == 'select':
                    code += self._js_elements[key].select() + "\n"
        code += "}\n"
        return code

    def __add__new_element(self):
        elem_name = "elem_cr" + str(len(self._js_elements))
        code = elem_name + " = " + JsDocument.createElement(random.choice(HtmlObjects.HTML_OBJECTS)) + "\n"
        self._js_elements[elem_name] = JsElement(elem_name)
        return elem_name, code

    def __add_element_method(self, key=None):
        code = ""
        if not key:
            key = random.choice(self._js_elements.keys())
        method = random.choice(DomObjects.DOM_ELEMENT_METHODS)
        if method == 'addEventListener':
            event = random.choice(DomObjects.DOM_EVENTS)
            self._occurring_events[event] += 1
            code += self._js_elements[key].addEventListener(event, event + "_handler")
        elif method == 'appendChild':
            if random.randint(1, 100) < 80:
                child = random.choice(self._js_elements.keys())
                if child == key:
                    elem_name, add_code = self.__add__new_element()
                    code += add_code
                    self._js_elements[elem_name] = JsElement(elem_name)
                    child = elem_name
                code += self._js_elements[key].appendChild(child)
            else:
                elem_name, add_code = self.__add__new_element()
                code += add_code
                self._js_elements[elem_name] = JsElement(elem_name)
                code += self._js_elements[key].appendChild(elem_name)
        elif method == 'cloneNode':
            length = len(self._js_elements)
            elem_name = "elem_cr" + str(length)
            code += elem_name + " = " + self._js_elements[key].cloneNode(True)
            self._js_elements[elem_name] = JsElement(elem_name)
            self._js_elements[elem_name].set_children(self._js_elements[key].get_children())
        elif method == 'hasAttribute':
            code += self._js_elements[key].hasAttribute(random.choice(HtmlObjects.HTML_ATTR_GENERIC))
        elif method == 'hasChildNode':
            code += self._js_elements[key].hasChildNodes()
        elif method == 'insertBefore':
            if not self._js_elements[key].get_children():
                elem_name, add_code = self.__add__new_element()
                code += add_code
                code += "\t" + self._js_elements[key].appendChild(elem_name) + "\n"
            elem_name, add_code = self.__add__new_element()
            code += add_code
            code += self._js_elements[key].insertBefore(elem_name, random.choice(self._js_elements[key].get_children()))
        elif method == 'normalize':
            code += self._js_elements[key].normalize()
        elif method == 'removeAttribute':
            if not self._js_elements[key].attributes:
                code += self._js_elements[key].setAttribute(random.choice(HtmlObjects.HTML_ATTR_GENERIC),
                                                            random.choice(FuzzValues.INTERESTING_VALUES))
            else:
                code += self._js_elements[key].removeAttribute(random.choice(self._js_elements[key].attributes.keys()))
        elif method == 'removeChild':
            if not self._js_elements[key].get_children():
                elem_name, add_code = self.__add__new_element()
                code += add_code
                code += self._js_elements[key].appendChild(elem_name)
            else:
                code += self._js_elements[key].removeChild(random.choice(self._js_elements[key].get_children()))
        elif method == 'replaceChild':
            if not self._js_elements[key].get_children():
                elem_name, add_code = self.__add__new_element()
                code += add_code
                code += self._js_elements[key].appendChild(elem_name)
            else:
                elem_name, add_code = self.__add__new_element()
                code += add_code
                code += self._js_elements[key].replaceChild(elem_name,
                                                            random.choice(self._js_elements[key].get_children()))
        elif method == 'removeEventListener':
            if not self._js_elements[key].registered_events:
                event = random.choice(DomObjects.DOM_EVENTS)
                self._occurring_events[event] += 1
                code += self._js_elements[key].addEventListener(event, event + "_handler")
            else:
                event = random.choice(self._js_elements[key].registered_events.keys())
                self._occurring_events[event] -= 1
                event = random.choice(self._js_elements[key].registered_events.keys())
                code += self._js_elements[key].removeEventListener(event,
                                                                   self._js_elements[key].registered_events[event])
        elif method == 'setAttribute':
            attr = random.choice(HtmlObjects.HTML_ATTR_GENERIC)
            if attr == 'style':
                val = ""
                for i in range(1, 50):
                    css = random.choice(FuzzValues.CSS_STYLES)
                    val += css[0] + ": " + random.choice(css[1:]) + "; "
            else:
                val = random.choice(FuzzValues.INTERESTING_VALUES)
            code += self._js_elements[key].setAttribute(attr, val)
        elif method == 'REPLACE_EXIST_ELEMENT':
            elem_name, add_code = self.__add__new_element()
            code += add_code
            code += "\t" + key + " = " + elem_name + ";"
            self._js_elements[key] = self._js_elements[elem_name]
        elif method == 'MIX_REFERENCES':
            code += self._js_elements[key]
        self._operations_count += 1
        return code
