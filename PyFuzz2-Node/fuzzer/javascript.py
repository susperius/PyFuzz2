__author__ = 'susperius'

# coding=utf8

from jsfuzzer.JsDocument import *
from jsfuzzer.JsElement import *
from jsfuzzer.JsAttrNodeMap import *
from jsfuzzer.domObjects import *
from jsfuzzer.htmlObjects import *
from jsfuzzer.values import *
from html import HtmlFuzzer
import random
import os

TEMPLATE_FILE = "fuzzer/jsfuzzer/template.dat"
NAME = "js_fuzzer"
CONFIG_PARAMS = ["starting_element", "total_operations", "browser", "seed"]


class JsFuzz:
    def __init__(self, starting_elements, total_operations, browser, seed=31337):
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
                depth = random.randint(0, self.__starting_element_count)
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

    @staticmethod
    def __get_html_ids(html):
        start = html.find("IDS:") + 5
        end = html.find("-->")
        ids = html[start:end].split("; ")
        del(ids[-1])
        return ids

    @staticmethod
    def __get_element(name, ident):
        return name + " = " + JsDocument.getElementById(ident)

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
        for i in range(count):
            code += "elem" + str(i) + " = " + JsDocument.createElement(random.choice(HtmlObjects.HTML_OBJECTS))
            self.__js_elements["elem" + str(i)] = (JsElement("elem" + str(i)), [], [], "")
        return code

    def __create_element_method_block(self):
        code = ""
        new_code = ""
        for i in range(self.__total_count):
            while new_code == "":
                new_code = self.__create_element_method()
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
            return ""
            event = random.choice(DomObjects.DOM_EVENTS_USABLE)
            events.append(event)
            code += elem.addEventListener(event, self.__event_listener)
        elif method == 'appendChild':
            new_key = "elem" + str(len(self.__js_elements))
            childs.append(new_key)
            self.__js_elements[new_key] = (JsElement(new_key), [], [], "")
            code += self.__create_element(new_key, random.choice(HtmlObjects.HTML_OBJECTS))
            code += "try{\n" + elem.appendChild(new_key) + "} catch(e){}\n"
        elif method == 'blur':
            code += "try{\n " + elem.blur() + "} catch(e){}\n"
        elif method == 'click':
            code += "try{\n " + elem.click() + "}catch(e){}\n"
        elif method == 'cloneNode':
            deep = random.choice(self.__bool)
            code += "try{\n " + elem.cloneNode(deep) + "} catch(e){}\n"
        elif method == 'compareDocumentPosition':
            code += "try{\n" + elem.compareDocumentPosition(random.choice(self.__js_elements.keys())) + "}catch(e){}\n"
        elif method == 'focus':
            code += "try{\n" + elem.focus() + "}catch(e){}\n"
        elif method == 'getAttribute':
            attr = random.choice(HtmlObjects.HTML_ATTR_GENERIC)
            code += "try{\n" + elem.getAttribute(attr) + "}catch(e){}\n"
        elif method == 'getAttributeNode':
            attr = random.choice(HtmlObjects.HTML_ATTR_GENERIC)
            code += "try{\n" + elem.getAttributeNode(attr) + "}catch(e){}\n"
        elif method == 'getElementsByClassName':
            if class_name == "":
                return ""
            code += "try{\n" + elem.getElementsByClassName(class_name) + "}catch(e){}\n"
        elif method == 'getElementsByTagName':
            if not self.__tag_names:
                return ""
            code += elem.getElementsByTagName(random.choice(self.__tag_names))
        elif method == 'getFeature':
            return ""
            code += ""
        elif method == 'getUserData':
            return ""
            code += ""
        elif method == 'hasAttribute':
            return ""
            code += ""
        elif method == 'hasAttributes':
            return ""
            code += ""
        elif method == 'hasChildNode':
            return ""
            code += ""
        elif method == 'insertBefore':
            return ""  # NEEDS DEBUGGING!
            if childs == []:
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
            code += "try{\n " + elem.normalize() + "}catch(e){}\n"
        elif method == 'querySelector':
            if class_name == "":
                return ""
            code += "try{\n " + elem.querySelector(class_name) + "}catch(e){}\n"
        elif method == 'querySelectorAll':
            if class_name == "":
                return ""
            code += "try{\n " + elem.querySelectorAll(class_name) + "}catch(e){}\n"
        elif method == 'removeAttribute':
            attr = random.choice(HtmlObjects.HTML_ATTR_GENERIC)
            if attr == "class":
                class_name = ""
            code += "try{\n " + elem.removeAttribute(attr) + "}catch(e){}\n"
        elif method == 'removeAttributeNode':
            return ""
            code += ""
        elif method == 'removeChild':
            if not childs:
                return ""
            child = random.choice(range(len(childs)))
            childs.remove(childs[child])
            code += "try{\n " + elem.removeChild(key + ".childNodes[" + str(child) + "]") + "} catch(e){}\n"
        elif method == 'replaceChild':
            if not childs:
                return ""
            child = random.choice(range(len(childs)))
            new_child = "elem" + str(len(self.__js_elements))
            code += self.__create_element(new_child, random.choice(HtmlObjects.HTML_OBJECTS))
            self.__js_elements[new_child] = (JsElement(new_child), [], [], "")
            code += "try{\n " + elem.replaceChild(new_child, key + ".childNodes[" + str(child) + "]") + "} catch(e){}\n"
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
            code += "try{\n " + elem.setAttribute(attr, value) + "} catch(e){}\n"
        elif method == 'setAttributeNode':
            return ""
            code += ""
        elif method == 'toString':
            code += "try{\n " + elem.toString() + "} catch(e){}\n"
        elif method == 'item':
            return ""
            code += ""
        elif method == 'REPLACE_EXIST_ELEMENT':
            code += key + " = " + JsDocument.createElement(random.choice(HtmlObjects.HTML_OBJECTS))
            childs = []
            events = []
            class_name = ""
        self.__js_elements[key] = (elem, childs, events, class_name)
        return code
