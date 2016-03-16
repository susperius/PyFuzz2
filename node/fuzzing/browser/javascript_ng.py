import random
import os

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
from model.JsWindow import JsWindow
from ..bytemutation import ByteMutation

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
    CONFIG_PARAMS = ['seed', 'starting_elements', 'html_depth', 'html_max_attr', 'canvas_size', 'js_block_size',
                     'function_count', 'file_type', 'media_folder']
    CALLING_COMMENT = "//CALLING COMMENT"
    FIRST_ARRAY_LENGTH = 5
    FUNCTION_TYPES = ['default', 'event', 'array']
    SPECIAL_PARAMETERS = ['JS_ARRAY', 'JS_DOM_CHILD_ELEMENT']

    def __init__(self, seed, starting_elements, html_depth, html_max_attr, canvas_size, js_block_size, function_count, file_type, media_folder="NONE"):
        self._html_fuzzer = Html5Fuzzer(int(seed), int(starting_elements), int(html_depth), int(html_max_attr), file_type)
        self._canvas_fuzzer = CanvasFuzzer(int(canvas_size))
        self._css_fuzzer = CssFuzzer(int(seed))
        random.seed(int(seed)) if int(seed) != 0 else random.seed()
        self._size = int(js_block_size)
        self._function_count = int(function_count)
        self._file_type = file_type
        self._js_objects = {}
        self._media_folder = media_folder
        self.__init_js_object_dict()
        self._js_default_functions = []
        self._js_event_listener = []
        self._js_array_functions = []
        max_funcs = min((self._size / 10), 20)
        for i in range(max_funcs):
            self._js_array_functions.append("array_func_" + str(i))
            self._js_event_listener.append("event_handler_" + str(i))
        self._html_page = HtmlPage()

    def __init_js_object_dict(self):
        for js_obj_type in JS_OBJECTS:
            self._js_objects[js_obj_type] = []

    @property
    def file_type(self):
        return self._file_type

    @classmethod
    def from_list(cls, params):
        return cls(params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8])

    @property
    def prng_state(self):
        return random.getstate

    def set_state(self, state):
        random.setstate(state)

    def create_testcases(self, count, directory):
        self.clear_folder(directory)
        media_file_names = []
        byte_mutation_fuzzers = []
        if self._media_folder is not "NONE":
            media_folder_listing = os.listdir(self._media_folder)
            for i in range(8):
                file_name = random.choice(media_folder_listing)
                media_file_names.append(file_name)
                byte_mutation_fuzzers.append(ByteMutation(self._media_folder + "/" + file_name, 5, 50, 0, file_name.split(".")[1]))
        for i in range(count):
            test_name = "/test" + str(i) if i > 9 else "/test0" + str(i)
            fuzzer_number = 0
            for byte_mutation_fuzzer in byte_mutation_fuzzers:
                fuzz_data_file_name = test_name + "_" + str(fuzzer_number) + "." + byte_mutation_fuzzer.file_type
                fuzz_data = byte_mutation_fuzzer.fuzz()
                with open(directory + fuzz_data_file_name, 'wb+') as data_fd:
                    data_fd.write(fuzz_data)
                self._html_fuzzer.add_embed_source(fuzz_data_file_name.replace("/", ""))
                fuzzer_number += 1
            with open(directory + test_name + "." + self._file_type, "wb+") as html_fd, open(directory + test_name + ".css", "wb+") as css_fd:
                html, css = self.fuzz()
                html = html.replace("TESTCASE", test_name)
                html_fd.write(html)
                css_fd.write(css)
            self._html_fuzzer.embed_sources_list = []

    def set_seed(self, seed):
        pass

    def __reinit(self):
        self._js_objects = {}
        self.__init_js_object_dict()
        self._js_default_functions = []

    def fuzz(self):
        self._html_page = self._html_fuzzer.fuzz()
        tags = self._html_page.get_elements_by_html_tag().keys()
        css_class_names = self._html_page.get_css_class_names()
        self._css_fuzzer.set_options(tags, css_class_names)
        css = self._css_fuzzer.fuzz()
        code = ""
        code += self.__init_js_objects(self._html_page)
        i = 0
        func_size = self._size / self._function_count
        while i < self._size:
            code += self.__build_function("default", func_size)
            i += func_size
        for func_name in self._js_event_listener:
            code += self.__build_function("event", func_size, func_name)
        for func_name in self._js_array_functions:
            code += self.__build_function("array", func_size, func_name)
        code += self.__add_event_dispatcher()
        call_block = ""
        for func_name in self._js_default_functions:
            choice = random.randint(1, 20)
            if choice < 15:
                call_block += "\t" + func_name + "();\n"
            else:
                call_block += "\t" + JsWindow.setTimeout(func_name + "();", 100) + "\n"
        call_block += "\t" + "event_firing();\n"
        call_block += "\t" + "location.reload();\n"
        code = code.replace(self.CALLING_COMMENT, call_block)
        html = self._html_page.get_raw_html()
        html = html.replace("SCRIPT_BODY", code)
        self.__reinit()
        return html, css

    def test(self):
        self._html_page = self._html_fuzzer.fuzz()
        tags = self._html_page.get_elements_by_html_tag().keys()
        css_class_names = self._html_page.get_css_class_names()
        self._css_fuzzer.set_options(tags, css_class_names)
        css = self._css_fuzzer.fuzz()
        code = ""
        code += self.__init_js_objects(self._html_page)
        for i in range(30):
            code += self.__build_assignment2() + "\n"
        return code

    def __init_js_objects(self, html_page):
        available_dom_elements = html_page.get_elements_by_id()
        code = "function startup() {\n"
        for element_id in available_dom_elements.keys():
            code += "\telem_" + element_id + " = " + JsDocument.getElementById(element_id) + ";\n"
            self._js_objects['JS_DOM_ELEMENT'].append(JsDomElement("elem_" + element_id,
                                                                   available_dom_elements[element_id]))
        #  Init a Object of each type
        for i in range(0, 5):
            code += "\t" + self.__build_js_array(self.FIRST_ARRAY_LENGTH)
            code += "\t" + self.__add_js_string()
            code += "\t" + self.__add_js_number()
            code += "\t" + self.__add_js_object()
        code += self.CALLING_COMMENT + "\n"
        code += "}\n"
        return code

    # region Little Helper
    def __build_js_array(self, length):
        array_obj_list = []
        for i in range(length):
            js_obj = self.__get_an_js_object()
            array_obj_list.append(js_obj)
        js_array = JsArray(self.__get_js_array_name(), array_obj_list)
        self._js_objects['JS_ARRAY'].append(js_array)
        return js_array.newArray() + ";\n"

    def __add_js_string(self):
        js_str = JsString(self.__get_js_string_name())
        self._js_objects['JS_STRING'].append(js_str)
        return js_str.newString(random.choice(FuzzValues.STRINGS)) + ";\n"

    def __add_js_number(self):
        js_number = JsNumber(self.__get_js_number_name())
        self._js_objects['JS_NUMBER'].append(js_number)
        return js_number.newNumber(random.choice(FuzzValues.INTS)) + ";\n"

    def __add_js_dom_element(self):
        var_name = "elem_" + str(len(self._js_objects['JS_DOM_ELEMENT']))
        html_type = random.choice(HTML5_OBJECTS.keys())
        js_dom_element = JsDomElement(var_name, html_type)
        self._js_objects['JS_DOM_ELEMENT'].append(js_dom_element)
        return var_name + " = " + JsDocument.createElement(html_type) + ";\n"

    def __add_js_object(self):
        var_name = self.__get_js_object_name()
        self._js_objects['JS_OBJECT'].append(JsObject(var_name))
        available_types = self._js_objects.keys()
        available_types.remove('JS_OBJECT')
        js_obj_type = random.choice(available_types)
        return var_name + " = " + (random.choice(self._js_objects[js_obj_type])).name + ";\n"

    def __get_js_dom_element_name(self):
        return "elem_" + str(len(self._js_objects['JS_DOM_ELEMENT']))

    def __get_js_string_name(self):
        return "str_" + str(len((self._js_objects['JS_STRING'])))

    def __get_js_number_name(self):
        return "number_" + str(len(self._js_objects['JS_NUMBER']))

    def __get_js_array_name(self):
        return "array_" + str(len(self._js_objects['JS_ARRAY']))

    def __get_js_object_name(self):
        return "object_" + str(len(self._js_objects['JS_OBJECT']))

    def __get_an_js_object(self):
        usable_object = self._js_objects.keys()
        usable_object.remove('JS_OBJECT')
        js_obj_type = 'JS_STRING' # random.choice(usable_object)
        while not self._js_objects[js_obj_type]:
            js_obj_type = random.choice(self._js_objects.keys())
        js_obj = random.choice(self._js_objects[js_obj_type])
        return js_obj

    @staticmethod
    def __check_params_for_optional(parameter_list):
        for param in parameter_list:
            if "*" in param:
                return True
        return False
    # endregion

    def __build_function(self, func_type, length, func_name=None):
        code = ""
        func_end = ""
        block_length = length / 10
        if func_type == 'default':
            func_name = "func_" + str(len(self._js_default_functions))
            self._js_default_functions.append(func_name)
            code += "function " + func_name + "() { \n"
            func_end = "}\n"
        elif func_type == "array" or "event":
            code += "function " + func_name + "(x) { \n"
            func_end = "\treturn x;\n}\n" if func_type == "array" else "}\n"
        for i in range(length):
            choice = random.randint(1, 20)
            if choice <= 10:
                code += "\t" + self.__build_assignment()
            elif 10 < choice < 15:
                code += self.__build_if_statement_block(block_length)
                i += block_length
            elif choice > 15:
                code += self.__build_for_loop_block(block_length)
                i += block_length
        code += func_end
        return code

    def __build_if_statement_block(self, length):
        code = "\tif " + self.__create_bool_expression() + "{ \n"
        for i in range(length):
            code += "\t\t" + self.__build_assignment(False)
        code += "\t}\n"
        return "\t" + JsGlobal.try_catch_block("\n" + code)

    #  TODO: iterate over the array
    def __build_for_loop_block(self, length):
        code = "\tfor (var i = 0; i < " + (random.choice(self._js_objects['JS_ARRAY'])).length() + ";i++) {\n"
        for i in range(length):
            code += "\t\t" + self.__build_assignment(False)
        code += "\t}\n"
        return "\t" + JsGlobal.try_catch_block("\n" + code)

    #  TODO: build assignments but keep the JsArray Objects functional (array elements)
    #  TODO: also keep the JsDomElement functional (children and so on)
    def __build_assignment2(self, try_catch=True):
        code = ""
        choice = random.randint(1, 20)
        js_obj = self.__get_an_js_object()
        js_method_name = random.choice(js_obj.methods_and_properties.keys())
        js_obj_method = js_obj.methods_and_properties[js_method_name]['method']
        js_method_ret_val = js_obj.methods_and_properties[js_method_name]['ret_val']
        js_method_parameters = js_obj.methods_and_properties[js_method_name]['parameters']
        special_param = (False, None)
        star_param = False
        if js_method_parameters is not None:
            for param in js_method_parameters:
                if param in self.SPECIAL_PARAMETERS:
                    special_param = (True, param)
                elif '*' in param:
                    star_param = True
        # region Default assignment
        if ((star_param and choice <= 10) or (not star_param)) and not special_param[0]:
            #  TODO: going deeper,
            #  TODO: e.g for strings call a method on a method call on method call and add it inside or outside
            if js_method_parameters is None or star_param:
                code += js_obj_method()
            else:
                parameters = self.__get_params(js_obj, js_method_parameters)
                code += js_obj_method(*parameters)
            js_method_ret_val = 'JS_NUMBER' if js_method_ret_val == "INT" or js_method_ret_val == "FLOAT" else js_method_ret_val
            if js_method_ret_val == "JS_DOM_ELEMENT":
                new_js_obj = JsDomElement(self.__get_js_dom_element_name()) if choice < 10 else random.choice(self._js_objects['JS_DOM_ELEMENT'])
                pass
            # region JS_STRING
            elif js_method_ret_val == "JS_STRING":
                new_js_obj = JsString(self.__get_js_string_name()) if choice < 10 else random.choice(self._js_objects['JS_STRING'])
                if choice > 15:
                    add_js_str_obj = random.choice(self._js_objects['JS_STRING'])
                    second_obj_code = add_js_str_obj.name
                    for i in range(choice % 10):
                        js_str_func = random.choice(js_obj.methods_and_properties_by_return_type['JS_STRING'])
                        add_js_str_func = random.choice(add_js_str_obj.methods_and_properties_by_return_type['JS_STRING'])
                        if js_str_func['parameters'] is not None and \
                                not self.__check_params_for_optional(js_str_func['parameters']):
                            js_str_func_parameters = self.__get_params(js_obj, js_str_func['parameters'])
                            code = "(" + code + ")" + (js_str_func['method'](*js_str_func_parameters)).replace(js_obj.name, "")
                        else:
                            code = "(" + code + ")" + (js_str_func['method']()).replace(js_obj.name, "")
                        if add_js_str_func['parameters'] is not None and \
                                not self.__check_params_for_optional(add_js_str_func['parameters']):
                            add_js_str_func_parameters = self.__get_params(js_obj, add_js_str_func['parameters'])
                            second_obj_code = "(" + second_obj_code + ")" + (add_js_str_func['method'](*add_js_str_func_parameters)).replace(add_js_str_obj.name, "")
                        else:
                            second_obj_code = "(" + second_obj_code + ")" + (add_js_str_func['method']()).replace(add_js_str_obj.name, "")
                    code = code + " + " + second_obj_code
            # endregion
            elif js_method_ret_val == "JS_NUMBER":
                new_js_obj = JsNumber(self.__get_js_number_name()) if choice < 10 else random.choice(self._js_objects['JS_NUMBER'])
                pass
            elif js_method_ret_val == "JS_ARRAY":
                new_js_obj = JsArray(self.__get_js_array_name()) if choice < 10 else random.choice(self._js_objects['JS_ARRAY'])
                pass
            else:  # it's a js_object
                new_js_obj = JsObject(self.__get_js_object_name()) if choice < 10 else random.choice(self._js_objects['JS_OBJECT'])
                pass
            code = new_js_obj.name + " = " + code
        #  endregion
        # region properties setting
        elif star_param and choice > 10:
            print("Star param")
            parameters = self.__get_params(js_obj, js_method_parameters)
            code = js_obj_method(*parameters)
        # endregion
        # region JS_ARRAY or JS_DOM_CHILD_ELEMENT
        elif special_param[0]:
            print("Special param")
            pass
        # endregion
        return code

    def __build_assignment(self, try_catch=True):
        choice = random.randint(1, 20)
        js_obj = self.__get_an_js_object()
        js_function_name = random.choice(js_obj.methods_and_properties.keys())
        if js_function_name == "removeChild" or js_function_name == "replaceChild":
            children = js_obj.get_children()
            if not children:
                js_function_name = "appendChild"
        js_obj_function = js_obj.methods_and_properties[js_function_name]
        parameters = js_obj_function['parameters']
        ret_val = js_obj_function['ret_val']
        optional = False
        if parameters is not None:
            for params in parameters:
                if "*" in params:
                    if choice > 8:
                        parameters = None
                    else:
                        optional = True
        if parameters is not None:
            params = self.__get_params(js_obj, js_obj_function['parameters'])
            code = js_obj_function['method'](*params)
        else:
            code = js_obj_function['method']()
        #  TODO: how to involve operators in numbers and strings ...
        if not optional:
            ret_val = "JS_STRING" if ret_val == "STRING" else ret_val
            ret_val = "JS_NUMBER" if ret_val == "INT" or ret_val == "EXP_FLOAT" or ret_val == "FLOAT" else ret_val
            if ret_val == "JS_DOM_ELEMENT":
                new_js_obj = JsDomElement(self.__get_js_dom_element_name()) if choice < 10 else random.choice(self._js_objects['JS_DOM_ELEMENT'])
                self._js_objects['JS_DOM_ELEMENT'].append(new_js_obj)
            elif ret_val == "JS_STRING":
                new_js_obj = JsString(self.__get_js_string_name()) if choice < 10 else random.choice(self._js_objects['JS_STRING'])
                self._js_objects['JS_STRING'].append(new_js_obj)
                if choice >= 15:
                    js_str = random.choice(self._js_objects['JS_STRING'])
                    js_str_func = random.choice(js_str.methods_and_properties_by_return_type['JS_STRING'])
                    js_str_func_params = self.__get_params(js_str, js_str_func['parameters']) if js_str_func['parameters'] is not None else None
                    code += " + " + js_str_func['method'](*js_str_func_params) if js_str_func['parameters'] is not None else " + " + js_str_func['method']()
            elif ret_val == "JS_NUMBER":
                new_js_obj = JsNumber(self.__get_js_number_name()) if choice < 10 else random.choice(self._js_objects['JS_NUMBER'])
                self._js_objects['JS_NUMBER'].append(new_js_obj)
                if choice >= 15:
                    number_operator = random.choice(JsNumber.OPERATORS)
                    js_number = random.choice(self._js_objects['JS_NUMBER'])
                    code += " " + number_operator + " " + js_number.name
            elif ret_val == "JS_ARRAY":
                new_js_obj = JsArray(self.__get_js_array_name()) if choice < 10 else random.choice(self._js_objects['JS_ARRAY'])
                self._js_objects['JS_ARRAY'].append(new_js_obj)
            else:
                new_js_obj = JsObject(self.__get_js_object_name()) if choice < 10 else random.choice(self._js_objects['JS_OBJECT'])
                self._js_objects['JS_OBJECT'].append(new_js_obj)
            code = new_js_obj.name + " = " + code
        return JsGlobal.try_catch_block(code + "; ") if try_catch else code + ";\n"

    def __get_params(self, calling_obj, param_list):
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
                ret_params.append(random.choice(DomObjectTypes.DOM_EVENTS))
            elif param == 'HTML_ATTR':
                html_attr = random.choice(HTML5_GLOBAL_ATTR.keys())
                ret_params.append(html_attr)
                if 'HTML_ATTR_VAL' in param_list:
                    if HTML5_GLOBAL_ATTR[html_attr] == "CSS_CLASS":
                        ret_params.append(random.choice(self._html_page.get_css_class_names()))
                    elif html_attr == "style":
                        style = random.choice(CSS_STYLES)
                        ret_params.append(style[0] + " " + random.choice(style[1:]))
                    else:
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
                    ret_params.append(random.choice(FuzzValues.PURE_INTS))
            elif param == 'JS_ARRAY':
                ret_params.append(random.choice(self._js_objects['JS_ARRAY']))
            elif param == 'JS_DOM_ELEMENT':
                ret_params.append((random.choice(self._js_objects['JS_DOM_ELEMENT'])).name)
            elif param == 'JS_DOM_CHILD_ELEMENT':
                if not calling_obj.get_children():
                    ret_params.append((random.choice(self._js_objects['JS_DOM_ELEMENT'])).name)
                else:
                    ret_params.append(random.choice(calling_obj.get_children()))
            elif param == 'JS_EVENT_LISTENER':
                ret_params.append(random.choice(self._js_event_listener))
            elif param == 'JS_ARRAY_FUNCTION':
                ret_params.append(random.choice(self._js_array_functions))
            elif param == 'JS_OBJECT':
                obj_type = random.choice(self._js_objects.keys())
                ret_params.append((random.choice(self._js_objects[obj_type])).name)
            elif param == 'LANG':
                ret_params.append(random.choice(FuzzValues.LANG_CODES))
            elif param == 'NAMESPACE_URI':
                # TODO: think about namespace URIs
                ret_params.append("localhost")
            elif param == 'NUMBER':
                ret_params.append(random.choice(FuzzValues.INTS))
            elif param == 'REGEX':
                # TODO: Build a regex builder method
                ret_params.append("g/[*]+/")
            elif param == 'JS_STRING':
                switch = random.choice([0, 1])
                if switch == 0:
                    ret_params.append((random.choice(self._js_objects['JS_STRING'])).name)
                else:
                    ret_params.append(random.choice(FuzzValues.STRINGS))
            elif param == 'TEXT_DIRECTION':
                ret_params.append(random.choice(FuzzValues.TEXT_DIRECTION))
            elif param == 'UNICODE_VALUE_LIST':
                value = random.randint(0x0000, 0xFFFF)
                ret_params.append(format(value, '04x'))
        return ret_params

    def __create_bool_expression(self):
        code = "("
        operator = random.choice(JsGlobal.BOOL_OPERATORS)
        operand_type = random.choice(self._js_objects.keys())
        operand1 = random.choice(self._js_objects[operand_type])
        operand2 = random.choice(self._js_objects[operand_type])
        same_ret_val = [x for x in operand1.methods_and_properties_by_return_type.keys() if x in operand2.methods_and_properties_by_return_type.keys()]
        ret_val = random.choice(same_ret_val)
        operand1_func = random.choice(operand1.methods_and_properties_by_return_type[ret_val])
        operand2_func = random.choice(operand2.methods_and_properties_by_return_type[ret_val])
        operand1_param = self.__get_params(operand1, operand1_func['parameters']) if operand1_func['parameters'] is not None and '*' not in ("" + x for x in operand1_func['parameters']) else None
        operand2_param = self.__get_params(operand2, operand2_func['parameters']) if operand2_func['parameters'] is not None and '*' not in ("" + x for x in operand2_func['parameters'])else None
        code += operand1_func['method'](*operand1_param) if operand1_param is not None else operand1_func['method']()
        code += operator
        code += operand2_func['method'](*operand2_param) if operand2_param is not None else operand2_func['method']()
        code += ")"
        return code

    def __add_event_dispatcher(self):
        code = "function event_firing() {\n"
        for elem in self._js_objects['JS_DOM_ELEMENT']:
            for event in elem.registered_events.keys():
                if 'DOM' in event:
                    continue
                elif event == 'click':
                    code += JsGlobal.try_catch_block(elem.click() + "\n", "ex")
                elif event == 'error':
                    pass
                elif event == 'load':
                    pass
                elif event == 'scroll':
                    code += JsGlobal.try_catch_block(elem.scrollLeft() + " = 10;" + "\n", "ex")
                elif event == 'resize' or event == 'change':
                    code += JsGlobal.try_catch_block(elem.innerHtml() + " = \"" + "A" * 100 + "\";\n", "ex")
                elif event == 'focus' or event == 'focusin':
                    code += JsGlobal.try_catch_block(elem.focus() + "\n", "ex")
                elif event == 'blur':
                    code += JsGlobal.try_catch_block(elem.blur() + "\n", "ex")
                elif event == 'select':
                    code += JsGlobal.try_catch_block(elem.select() + "\n", "ex")
        code += "}\n"
        return code
