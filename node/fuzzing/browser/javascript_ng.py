import random

from html5 import Html5Fuzzer
from canvas import CanvasFuzzer
from css import CssFuzzer
from ..fuzzer import Fuzzer
from model.JsDocument import JsDocument
from model.JsObject import *
from model.JsDomElement import *
from model.values import FuzzValues

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
    FIRST_ARRAY_LENGTH = 5

    def __init__(self, seed, starting_elements, html_depth, html_max_attr, canvas_size, file_type):
        self._html_fuzzer = Html5Fuzzer(seed, starting_elements, html_depth, html_max_attr, file_type)
        self._canvas_fuzzer = CanvasFuzzer(canvas_size)
        self._css_fuzzer = CssFuzzer(seed)
        random.seed(0)
        self._file_type = file_type
        self._js_objects = {}
        self.__init_js_object_dict()
        self._js_event_listener = []
        self._js_array_functions = []

    def __init_js_object_dict(self):
        for js_obj_type in JS_OBJECTS:
            self._js_objects[js_obj_type] = []

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
        code += self.__init_js_objects(html_page)
        for i in range(20):
            code += self.__build_assignment()
        return code

    def __init_js_objects(self, html_page):
        available_dom_elements = html_page.get_elements_by_id()
        code = "function startup() {\n"
        for element_id in available_dom_elements.keys():
            code += "\telem_" + element_id + " = " + JsDocument.getElementById(element_id) + ";\n"
            self._js_objects['JS_DOM_ELEMENT'].append(JsDomElement("elem_" + element_id,
                                                                   available_dom_elements[element_id]))
        code += self.__build_js_array(self.FIRST_ARRAY_LENGTH)
        code += "\t" + self.CALLING_COMMENT + "\n"
        return code

    def __build_js_array(self, length):
        array_obj_list = []
        for i in range(length):
            js_obj = self.__get_an_js_object()
            array_obj_list.append(js_obj)
        js_array = JsArray("array_" + str(len(self._js_objects['JS_ARRAY'])), array_obj_list)
        self._js_objects['JS_ARRAY'].append(js_array)
        return js_array.newArray()

    def __build_assignment(self):
        code, ret_val = self.__create_a_method_or_prop_call()
        if ret_val in JS_OBJECTS or ret_val in ['STRING', 'INT']:
            assignment_obj = None
            what_do_to_next = random.choice(['REPLACE_AN_EXISTING_OBJ', 'CREATE_A_NEW_OBJ'])
            if what_do_to_next == "REPLACE_AN_EXISTING_OBJ":
                assignment_obj = random.choice(self._js_objects[ret_val])
                code = assignment_obj.name + " = " + code + ";\n"
            elif what_do_to_next == "CREATE_A_NEW_OBJ":
                assignment_obj_name = "elem_" + str(len(self._js_objects))
                if ret_val == "JS_STRING" or ret_val == "STRING":
                    assignment_obj = JsString(assignment_obj_name)
                elif ret_val == "JS_ARRAY":
                    assignment_obj = JsArray(assignment_obj_name, [])
                elif ret_val == "JS_NUMBER" or ret_val == "INT":
                    assignment_obj = JsNumber(assignment_obj_name)
                elif ret_val == "JS_DOM_ELEMENT":
                    assignment_obj = JsDomElement(assignment_obj_name, "")
                self._js_objects[ret_val].append(assignment_obj)
            code = assignment_obj.name + " = " + code + ";\n"
        else:
            code += ";\n"
        return code

    def __create_a_method_or_prop_call(self):
        js_obj = self.__get_an_js_object()
        js_obj_function = js_obj.methods_and_properties[random.choice(js_obj.methods_and_properties.keys())]
        if js_obj_function['parameters'] is not None:
            params = self.__get_params(js_obj_function['parameters'])
            code = js_obj_function['method'](*params)
        else:
            code = js_obj_function['method']()
        return code, js_obj_function['ret_val']

    def __get_an_js_object(self):
        js_obj_type = random.choice(self._js_objects.keys())
        while not self._js_objects[js_obj_type]:
            js_obj_type = random.choice(self._js_objects.keys())
        js_obj = random.choice(self._js_objects[js_obj_type])
        return js_obj

    def __get_params(self, param_list):
        ret_params = []
        print(param_list)
        for param in param_list:
            if param == "STRING":
                str_src = random.choice([0, 1, 2])
                if str_src == 0:  # Take one from FuzzValues
                    ret_params.append(FuzzValues.STRINGS)
                elif str_src == 1:  # Create a JsString
                    ret_params.append(self.__create_js_string())
                elif str_src == 2:
                    key = random.choice(self._js_objects.keys())
                    while not self._js_objects[key]:  # Find a object
                        key = random.choice[key]
                    ret_params.append(self._js_objects[key].toString())
            elif param == "INT":
                ret_params.append(random.choice(FuzzValues.INTS))
            elif param == "NUMBER":  # as string in expo writing or or or
                value = random.choice(FuzzValues.INTS)
                as_string = random.choice([0, 1])
                if as_string == 1:
                    value = "\"" + value + "\""
                ret_params.append(value)
            elif param == "JS_ARRAY":
                ret_params.append(random.choice(self._js_objects['JS_ARRAY']))
            elif param == "JS_FUNCTION":
                if not self._js_array_functions:
                    pass  # TODO: Build a function!
                else:
                    ret_params.append(random.choice(self._js_array_functions))
        return ret_params

    def __create_js_string(self):
        x = self._js_objects
        return ""




