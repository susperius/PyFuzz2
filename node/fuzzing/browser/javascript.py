__author__ = 'susperius'

import random

from jsfuzzer.JsDocument import *
from jsfuzzer.JsElement import *
from jsfuzzer.JsGlobal import JsGlobal
from jsfuzzer.domObjects import *
from jsfuzzer.htmlObjects import *
from jsfuzzer.JsWindow import *
from html5 import Html5Fuzzer
from css import CssFuzzer
from canvas import CanvasFuzzer
from jsfuzzer.values import FuzzValues
from jsfuzzer.cssProperties import CSS_STYLES
from ..fuzzer import Fuzzer

TEMPLATE_FILE = "fuzzing/jsfuzzer/template.dat"


class JsDomFuzzer(Fuzzer):
    NAME = "js_dom_fuzzer"
    CONFIG_PARAMS = ["starting_elements", "total_operations", "browser", "seed", "canvas_size", "file_type"]

    def __init__(self, starting_elements, total_operations, browser, seed, canvas_size, file_type='html'):
        self._starting_elements = int(starting_elements)
        self._total_operations = int(total_operations)
        self._browser = browser
        seed = int(seed)
        #  self._html_fuzzer = HtmlFuzzer(self._starting_elements, 3, seed)
        self._html_fuzzer = Html5Fuzzer(int(seed), self._starting_elements, 10, 5, file_type)
        self._css_fuzzer = CssFuzzer(seed)
        self._canvas_fuzzer = CanvasFuzzer(int(canvas_size))
        if seed == 0:
            random.seed()
        else:
            random.seed(seed)
        self._file_type = file_type
        self._function_count = 0
        self._operations_count = 0
        self._js_elements = {}
        """:type dict(JsElement)"""
        self._window_timeout = 20
        self._occurring_events = {}
        for event in DomObjects.DOM_EVENTS:
            self._occurring_events[event] = 0

    @classmethod
    def from_list(cls, params):
        return cls(params[0], params[1], params[2], params[3], params[4], params[5])

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

    def set_seed(self, seed=0):
        random.seed(seed)

    def __reinit(self):
        self._function_count = 0
        self._operations_count = 0
        self._function_count = 0
        self._operations_count = 0
        self._js_elements = {}
        """:type dict(JsElement)"""
        self._window_timeout = 20
        self._occurring_events = {}
        for event in DomObjects.DOM_EVENTS:
            self._occurring_events[event] = 0

    def create_testcases(self, count, directory):
        for i in range(count):
            test_name = "/test" + str(i) if i > 9 else "/test0" + str(i)
            with open(directory + test_name + "." + self._file_type, "wb+") as html_fd, open(directory + test_name + ".css", "wb+") as css_fd:
                html, css = self.fuzz()
                html = html.replace("TESTCASE", test_name)
                html_fd.write(html)
                css_fd.write(css)

    def fuzz(self):
        html = self._html_fuzzer.fuzz()
        self._css_fuzzer.set_tags(self._html_fuzzer.tags)
        css = self._css_fuzzer.fuzz()
        ids = self._html_fuzzer.elem_ids
        js_code = ""
        for canvas_id in self._html_fuzzer.canvas_ids:
            self._canvas_fuzzer.set_canvas_id(canvas_id)
            js_code += self._canvas_fuzzer.fuzz()
        js_code += self.__create_startup(ids)

        while self._total_operations > self._operations_count:
            js_code += self.__add_function()
        js_code += self.__last_function()
        js_code += self.__add_event_dipatcher()
        js_code += self.__add_event_handlers()
        doc = html.replace("SCRIPT_BODY", js_code)
        self.__reinit()
        return doc, css

    def set_state(self, state):
        random.setstate(state)

    def __last_function(self):
        code = "function func" + str(self._function_count) + "(){ \r\n"
        code += "\tevent_firing();\r\n"
        code += "}\r\n"
        return code

    def __create_startup(self, elem_ids):
        code = "function startup() {\n"
        i = 0
        for elem_id in elem_ids:
            code += "\t" + "elem" + str(i) + " = " + JsDocument.getElementById(elem_id) + "\n"
            self._js_elements["elem"+str(i)] = JsElement("elem"+str(i))
            i += 1
        for canvas_id in self._html_fuzzer.canvas_ids:
            code += "\t" + JsWindow.setTimeout("func_" + canvas_id + "()", self._window_timeout)
        code += "\t" + JsWindow.setTimeout("func0" + "()", self._window_timeout) + "\n}\n"
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
            code += "\t" + JsWindow.setTimeout("func" + str(self._function_count) + "()", self._window_timeout + 100) + " \n"
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
                if 'DOM' in event:
                    continue
                elif event == 'click':
                    code += JsGlobal.try_catch_block(self._js_elements[key].click() + "\n", "ex")
                elif event == 'error':
                    pass
                elif event == 'load':
                    pass
                elif event == 'scroll':
                    code += JsGlobal.try_catch_block(self._js_elements[key].prop_scrollLeft() + " = 10;" + "\n", "ex")
                elif event == 'resize' or event == 'change':
                    code += JsGlobal.try_catch_block(self._js_elements[key].prop_innerHtml() + " = \"" + "A" * 100 + "\";\n", "ex")
                elif event == 'focus' or event == 'focusin':
                    code += JsGlobal.try_catch_block(self._js_elements[key].focus() + "\n", "ex")
                elif event == 'blur':
                    code += JsGlobal.try_catch_block(self._js_elements[key].blur() + "\n", "ex")
                elif event == 'select':
                    code += JsGlobal.try_catch_block(self._js_elements[key].select() + "\n", "ex")
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
        method = random.choice(DomObjects.DOM_ELEMENT_FUZZ_STUFF)
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
                    css = random.choice(CSS_STYLES)
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
        elif method == 'className':
            code += self._js_elements[key].prop_className() + " = \"" + random.choice(FuzzValues.STRINGS) + "\";"
        elif method == 'contentEditable':
            code += self._js_elements[key].prop_contentEditable() + " = " + random.choice(FuzzValues.BOOL) + ";"
        elif method == 'dir':
            code += self._js_elements[key].prop_dir() + " = \"" + random.choice(FuzzValues.TEXT_DIRECTION) + "\";"
        elif method == 'id':
            code += self._js_elements[key].prop_id() + " = \"" + random.choice(FuzzValues.STRINGS) + "\";"
        elif method == 'innerHTML':
            code += self._js_elements[key].prop_innerHtml() + " = \"" + random.choice(FuzzValues.STRINGS) + "\";"
        elif method == 'lang':
            code += self._js_elements[key].prop_lang() + " = \"" + random.choice(FuzzValues.LANG_CODES) + "\";"
        elif method == 'scrollLeft':
            code += self._js_elements[key].prop_scrollLeft() + " = \"" + random.choice(FuzzValues.INTS) + "\";"
        elif method == 'scrollTop':
            code += self._js_elements[key].prop_scrollTop() + " = \"" + random.choice(FuzzValues.INTS) + "\";"
        elif method == 'style':
            value = random.choice(CSS_STYLES)
            if "-" in value[0]:
                pos = value[0].find("-")
                value[0] = value[0].replace("-", "")
                value[0] = value[0][0:pos-1] + value[0][pos].upper() + value[0][pos+1:]
            code += self._js_elements[key].prop_style() + "." + value[0] + " = \"" + random.choice(value[1:]) + "\";"
        elif method == 'tabIndex':
            code += self._js_elements[key].prop_tabIndex() + " = " + str(random.randint(-20, 20)) + ";"
        elif method == 'textContent':
            code += self._js_elements[key].prop_textContent() + " = \"" + random.choice(FuzzValues.STRINGS) + "\";"
        elif method == 'title':
            code += self._js_elements[key].prop_title() + " = \"" + random.choice(FuzzValues.STRINGS) + "\";"
        self._operations_count += 1
        if random.randint(1, 10000) < 50:
            code += "CollectGarbage();"
        return code
