__author__ = 'susperius'

# coding=utf8

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

class JsFuzz(fuzzer.Fuzzer):
    NAME = "js_fuzzer"
    CONFIG_PARAMS = ["starting_element", "total_operations", "browser", "seed", "file_type"]

    def __init__(self, starting_elements, total_operations, browser, seed=31337, file_type="html"):
        self.__js_elements = {}
        self.__js_attributes = []
        self.__bool = ['true', 'false']
        self.__tag_names = []
        self.__starting_element_count = starting_elements
        self.__total_count = total_operations
        self.__event_listener = "dummy"
        self.__browser = browser
        self.__html_fuzzer = None
        self.__seed = seed
        self.__file_type = file_type
        if seed == 0:
            random.seed()
        else:
            random.seed(seed)

    def __set_start_values(self):
        self.__js_elements = {}
        self.__js_attribute = []
        self.__tag_names = []

    def fuzz(self, use_default_template=False):
        if use_default_template:
            startup = self.__create_elements(self.__starting_element_count)
            startup += self.__create_element_method_block()
            with open(TEMPLATE_FILE, 'r') as fd:
                templ = fd.read()
        else:
            if self.__html_fuzzer is None:
                depth = random.randint(0, random.randint(1, 11))
                self.__html_fuzzer = HtmlFuzzer(self.__starting_element_count, depth, self.__seed)
            startup = ""
            html_file = self.__html_fuzzer.fuzz()
            html_id = self.__get_html_ids(html_file)
            startup += self.__get_elements(html_id)
            startup += self.__create_element_method_block()
            templ = html_file
        templ = templ.replace("START_UP", startup)
        templ = templ.replace("SCRIPT_BODY", "")
        templ = templ.replace("EVENT_HANDLER", "")
        self.__set_start_values()
        return templ

    @property
    def prng_state(self):
        return random.getstate()

    @property
    def file_type(self):
        return self.__file_type

    def set_state(self, state):
        random.setstate(state)

    @staticmethod
    def __get_html_ids(html):
        start = html.find("IDS:") + 5
        end = html.find("-->")
        ids = html[start:end].split("; ")
        del(ids[-1])
        return ids

    @staticmethod
    def __get_element(name, ident):
        return name + " = " + JsDocument.getElementById(ident) + "\n"

    def __get_elements(self, html_ids):
        code = ""
        i = 0
        for ident in html_ids:
            code += self.__get_element("elem" + str(i), ident)
            self.__js_elements["elem" + str(i)] = (JsElement("elem" + str(i)), [], [], "")
            i += 1
        return code

    @staticmethod
    def __create_element(name, html_obj):
        return name + " = " + JsDocument.createElement(html_obj)

    def __create_elements(self, count):
        code = ""
        code += "doc_body = " + JsDocument.getElementById("doc_body") + "\n"
        body = JsElement("doc_body")
        for i in range(count):
            code += "elem" + str(i) + " = " + JsDocument.createElement(random.choice(HtmlObjects.HTML_OBJECTS)) + "\n"
            code += body.appendChild("elem" + str(i)) + "\n"
            self.__js_elements["elem" + str(i)] = (JsElement("elem" + str(i)), [], [], "")
        return code

    def __create_element_method_block(self):
        code = ""
        new_code = ""
        for i in range(self.__total_count):
            while new_code == "":
                new_code = JsGlobal.try_catch_block(self.__create_element_method(), "e")
            if self.__browser == "ie":
                x = random.choice(range(1000))
                if x < 10:
                    new_code += "CollectGarbage();\n"
            code += new_code
            new_code = ""
        return code

    def __create_element_method(self):
        code = ""
        method = random.choice(DomObjects.DOM_ELEMENT_METHODS)
        key = random.choice(self.__js_elements.keys())
        elem, childs, events, class_name = self.__js_elements[key]
        if method == 'addEventListener':
            event = random.choice(DomObjects.DOM_EVENTS_USABLE)
            events.append(event)
            code += elem.addEventListener(event, self.__event_listener)
        elif method == 'appendChild':
            new_key = "elem" + str(len(self.__js_elements))
            childs.append(new_key)
            self.__js_elements[new_key] = (JsElement(new_key), [], [], "")
            code += self.__create_element(new_key, random.choice(HtmlObjects.HTML_OBJECTS)) + "\n"
            code += elem.appendChild(new_key)
        elif method == 'blur':
            code += elem.blur()
        elif method == 'click':
            code += elem.click()
        elif method == 'cloneNode':
            deep = random.choice(self.__bool)
            code += elem.cloneNode(deep)
        elif method == 'compareDocumentPosition':
            code += elem.compareDocumentPosition(random.choice(self.__js_elements.keys()))
        elif method == 'focus':
            code += elem.focus()
        elif method == 'getAttribute':
            attr = random.choice(HtmlObjects.HTML_ATTR_GENERIC)
            code += elem.getAttribute(attr)
        elif method == 'getAttributeNode':
            attr = random.choice(HtmlObjects.HTML_ATTR_GENERIC)
            code += elem.getAttributeNode(attr)
        elif method == 'getElementsByClassName':
            if class_name == "":
                return ""
            code += elem.getElementsByClassName(class_name)
        elif method == 'getElementsByTagName':
            if not self.__tag_names:
                return ""
            code += elem.getElementsByTagName(random.choice(self.__tag_names))
        elif method == 'getFeature':
            code += elem.getFeature()
            return ""
        elif method == 'getUserData':
            code += elem.getUserData()
            return ""
        elif method == 'hasAttribute':
            code += elem.hasAttribute(random.choice(HtmlObjects.HTML_ATTR_GENERIC))
        elif method == 'hasAttributes':
            code += elem.hasAttributes()
        elif method == 'hasChildNode':
            code += elem.hasChildNodes()
        elif method == 'insertBefore':
            if not childs:
                return ""
            new_key = "elem" + str(len(self.__js_elements))
            childs.append(new_key)
            self.__js_elements[new_key] = (JsElement(new_key), [], [], "")
            code += JsDocument.createElement(random.choice(HtmlObjects.HTML_OBJECTS))
            code += elem.insertBefore(new_key, random.choice(childs))
        elif method == 'isDefaultNameSpace':
            return ""
            code += ""
        elif method == 'isEqualNode':
            return ""
            code += ""
        elif method == 'isSameNode':
            return ""
            code += ""
        elif method == 'isSupported':
            return ""
            code += ""
        elif method == 'normalize':
            code += elem.normalize()
        elif method == 'querySelector':
            if class_name == "":
                return ""
            code += elem.querySelector(class_name)
        elif method == 'querySelectorAll':
            if class_name == "":
                return ""
            code += elem.querySelectorAll(class_name)
        elif method == 'removeAttribute':
            attr = random.choice(HtmlObjects.HTML_ATTR_GENERIC)
            if attr == "class":
                class_name = ""
            code += elem.removeAttribute(attr)
        elif method == 'removeAttributeNode':
            return ""
            code += ""
        elif method == 'removeChild':
            if not childs:
                return ""
            child = random.choice(range(len(childs)))
            childs.remove(childs[child])
            code += elem.removeChild(key + ".childNodes[" + str(child) + "]")
        elif method == 'replaceChild':
            if not childs:
                return ""
            child = random.choice(range(len(childs)))
            new_child = "elem" + str(len(self.__js_elements))
            code += self.__create_element(new_child, random.choice(HtmlObjects.HTML_OBJECTS))
            self.__js_elements[new_child] = (JsElement(new_child), [], [], "")
            code += elem.replaceChild(new_child, key + ".childNodes[" + str(child) + "]")
            childs.remove(childs[child])
            childs.append(new_child)
        elif method == 'removeEventListener':
            if not events:
                return ""
            event = random.choice(events)
            events.remove(event)
            code += elem.removeEventListener(event, self.__event_listener)
        elif method == 'setAttribute':
            attr = random.choice(HtmlObjects.HTML_ATTR_GENERIC)
            value = random.choice(FuzzValues.INTERESTING_VALUES)
            if attr == 'class':
                class_name = value
            elif attr == 'style':
                css_pack = random.choice(FuzzValues.CSS_STYLES)
                value = css_pack[0] + "=" + random.choice(css_pack[1:])
            code += elem.setAttribute(attr, value)
        elif method == 'setAttributeNode':
            return ""
            code += ""
        elif method == 'toString':
            code += elem.toString()
        elif method == 'item':
            return ""
            code += ""
        elif method == 'REPLACE_EXIST_ELEMENT':
            code += key + " = " + JsDocument.createElement(random.choice(HtmlObjects.HTML_OBJECTS))
            childs = []
            events = []
            class_name = ""
        elif method == 'MIX_REFERENCES':
            mixed_obj = random.choice(self.__js_elements.keys())
            code += key + " = " + mixed_obj + ";"
            elem, childs, events, class_name = self.__js_elements[mixed_obj]
        self.__js_elements[key] = (elem, childs, events, class_name)
        return code
