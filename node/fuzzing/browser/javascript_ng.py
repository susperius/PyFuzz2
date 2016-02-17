import random

from html5 import Html5Fuzzer
from canvas import CanvasFuzzer
from css import CssFuzzer
from ..fuzzer import Fuzzer
from model.JsDocument import JsDocument
from model.JsObject import *
from model.JsDomElement import *
from model.JsGlobal import JsGlobal
from model.values import FuzzValues
from model.HtmlObjects import *
from model.CssProperties import CSS_STYLES
from model.DomObjectTypes import DomObjectTypes
from model.FuzzedHtmlPage import HtmlPage

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
# TODO: Method for array function; Method for event listener
#
#
#
#


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
        self._html_page = HtmlPage()
        self._values_dict = {'BOOL',
                             'CLASS_NAME',
                             'CSS_SELECTOR',
                             'CSS_STYLE',
                             'EVENT',
                             'HTML_ATTR',
                             'HTML_ATTR_VAL',
                             'HTML_CODE*',
                             'HTML_TAG',
                             'INT',
                             'INT*',
                             'JS_ARRAY',
                             'JS_DOM_CHILD_ELEMENT',
                             'JS_DOM_ELEMENT',
                             'JS_EVENT_LISTENER',
                             'JS_FUNCTION',
                             'JS_OBJECT',
                             'LANG_CODE*',
                             'NAMESPACE_URI',
                             'NUMBER',
                             'REGEX',
                             'STRING',
                             'STRING*',
                             'TEXT_DIRECTION*',
                             'UNICODE_VALUE_LIST'}

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
        self._html_page = self._html_fuzzer.fuzz()
        tags = self._html_page.get_elements_by_html_tag().keys()
        css_class_names = self._html_page.get_css_class_names()
        self._css_fuzzer.set_options(tags, css_class_names)
        css = self._css_fuzzer.fuzz()
        code = ""
        code += self.__init_js_objects(self._html_page)
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
            #  TODO: Fix the naming inconsistency
            if ret_val == 'STRING':
                ret_val = 'JS_STRING'
            elif ret_val == 'INT':
                ret_val = 'JS_NUMBER'
            assignment_obj = None
            what_do_to_next = random.choice(['REPLACE_AN_EXISTING_OBJ', 'CREATE_A_NEW_OBJ']) if self._js_objects[
                ret_val] else 'CREATE_A_NEW_OBJ'
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
        #  TODO: Handle the * in parameter list !!!!!!!! <----- GO ON HERE !!!!
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
        for param in param_list:
            if param == 'BOOL':
                switch = random.choice([0, 1])
                if switch == 0:
                    ret_params.append(self.__create_bool_expression())
                elif switch == 1:
                    ret_params.append(random.choice(FuzzValues.BOOL))
            elif param == 'CLASS_NAME':
                ret_params.append(random.choice(self._html_page.get_css_class_names()))
            elif param == 'CSS_SELECTOR':  # Build a tag, tag, tag style selector
                # TODO: Work through the CSS Selector reference
                count = random.randint(1, 10)
                css_selector = ""
                for i in range(count):
                    css_selector += random.choice(self._html_page.get_elements_by_html_tag().keys()) + ","
                css_selector = css_selector[:-1]  # remove the comma
                ret_params.append(random.choice(css_selector))
            elif param == 'CSS_STYLE':
                style = random.choice(CSS_STYLES)
                ret_params.append(style[0])
                ret_params.append(random.choice(style[1:]))
            elif param == 'EVENT':
                ret_params.append(DomObjectTypes.DOM_EVENTS)
            elif param == 'HTML_ATTR':
                html_attr = random.choice(HTML5_GLOBAL_ATTR.keys())
                ret_params.append(html_attr)
                if 'HTML_ATTR_VAL' in param_list:
                    ret_params.append(random.choice(Html5Fuzzer.TYPES_DICT[HTML5_GLOBAL_ATTR[html_attr]]))
            elif param == 'HTML_ATTR_VAL':
                continue
            elif param == 'HTML_CODE':
                count = random.randint(1, 10)
                ret_params.append(self._html_fuzzer.get_some_html_code(count))
            elif param == 'HTML_TAG':
                ret_params.append(random.choice(HTML5_OBJECTS.keys()))
            elif param == 'INT':
                switch = random.choice([0, 1])
                if switch == 1:  # Get a JS_Number ID
                    ret_params.append((random.choice(self._js_objects['JS_NUMBER'])).name)
                else:  # Get one from FuzzValues
                    ret_params.append(FuzzValues.PURE_INTS)
            elif param == 'JS_ARRAY':
                ret_params.append((random.choice(self._js_objects['JS_ARRAY'])).name)
            elif param == 'JS_DOM_ELEMENT' or param == 'JS_DOM_CHILD_ELEMENT':
                ret_params.append((random.choice(self._js_objects['JS_DOM_ELEMENT'])).name)
            elif param == 'JS_EVENT_LISTENER':
                listener_name = "event_listner_" + str(len(self._js_event_listener))
                self._js_event_listener.append(listener_name)
                ret_params.append(listener_name)
            elif param == 'JS_ARRAY_FUNCTION':
                function_name = "array_function_" + str(len(self._js_array_functions))
                self._js_array_functions.append(function_name)
                ret_params.append(function_name)
            elif param == 'JS_OBJECT':
                obj_type = random.choice(self._js_objects.keys())
                ret_params.append((random.choice(self._js_objects[obj_type])).name)
            elif param == 'LANG':
                ret_params.append(random.choice(FuzzValues.LANG_CODES))
            elif param == 'NAMESPACE_URI':
                # TODO: think about namespace URIs
                ret_params.append("localhost")
            elif param == 'NUMBER':
                ret_params.append(random.choice(FuzzValues.INTERESTING_VALUES))
            elif param == 'REGEX':
                # TODO: Build a regex builder method
                ret_params.append("g/*/")
            elif param == 'STRING':
                switch = random.choice([0, 1])
                if switch == 0:
                    ret_params.append((random.choice(self._js_objects['JS_STRING'])).name)
                else:
                    ret_params.append(random.choice(FuzzValues.STRINGS))
            elif param == 'TEXT_DIRECTION':
                ret_params.append(random.choice(FuzzValues.TEXT_DIRECTION))
            elif param == 'UNICODE_VALUE_LIST':
                value = random.randint(0x0000, 0xFFFF)
                ret_params.append(value)
        return param_list

    def __create_js_string(self):
        x = self._js_objects
        return ""

    def __create_bool_expression(self):
        code = "("
        operator = random.choice(JsGlobal.BOOL_OPERATORS)
        operand_type = random.choice(self._js_objects.keys())
        operand1 = random.choice(self._js_objects[operand_type])
        operand2 = random.choice(self._js_objects[operand_type])
        same_ret_val = [x for x in operand1.methods_and_properties_by_type.keys() if x in operand2.methods_and_properties_by_type.keys()]
        ret_val = random.choice(same_ret_val)
        operand1_func = random.choice(operand1.methods_and_properties_by_type[ret_val])
        operand2_func = random.choice(operand2.methods_and_properties_by_type[ret_val])
        operand1_param = self.__get_params(operand1_func['parameters']) if operand1_func['parameters'] is not None else None
        operand2_param = self.__get_params(operand2_func['parameters']) if operand2_func['parameters'] is not None else None
        code += operand1_func['method'](*operand1_param) if operand1_param is not None else operand1_func['method']()
        code += operator
        code += operand1_func['method'](*operand2_param) if operand2_param is not None else operand2_func['method']()
        code += ")"
        return code
