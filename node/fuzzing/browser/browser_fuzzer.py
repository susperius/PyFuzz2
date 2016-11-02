import random
from html5 import Html5Fuzzer
from canvas import CanvasFuzzer
from css import CssFuzzer
from ..fuzzer import Fuzzer
from model.FuzzedHtmlPage import HtmlPage
from model.JsObject import *
from model.JsDocument import JsDocument
from model.JsDomElement import JsDomElement
from model.values import FuzzValues
from model.HtmlObjects import HTML5_OBJECTS


class BrowserFuzzer(Fuzzer):
    NAME = "browser_fuzzer"
    CONFIG_PARAMS = ["html_elements", "max_html_depth", "max_html_attr", "canvas_size", "canvas_type",
                     "js_function_count", "js_function_size", "file_type"]
    CALLING_BLOCK_COMMENT = "//CALLFUNCTIONS"

    def __init__(self, html_elements, max_html_depth, max_html_attr, canvas_size, canvas_type,
                 js_function_count, js_function_size, file_type):
        self._html_fuzzer = Html5Fuzzer(0, html_elements, max_html_depth, max_html_attr, file_type)
        self._canvas_fuzzer = CanvasFuzzer(canvas_size, canvas_type)
        self._css_fuzzer = CssFuzzer(0)
        self._js_function_count = js_function_count
        self._js_function_size = js_function_size
        self._html_page = HtmlPage()
        self._js_functions = []
        self._js_objects = {}
        self._file_type = file_type
        self._method_call_depth = 0

    def __init_js_objects_dict(self):
        for obj_type in JS_OBJECTS:
            self._js_objects[obj_type] = []

    def __reinit(self):
        self._js_functions = []
        self._js_objects = {}
        self.__init_js_objects_dict()

    def set_seed(self, seed):
        pass

    def prng_state(self):
        pass

    def file_type(self):
        return self._file_type

    @staticmethod
    def clear_folder(folder):
        Fuzzer.clear_folder(folder)

    def create_testcases(self, count, directory):
        pass

    @classmethod
    def from_list(cls, params):
        pass

    def set_state(self, state):
        pass

    def fuzz(self):
        self.__reinit()
        js_code = ""
        self._html_page = self._html_fuzzer.fuzz()
        self._css_fuzzer.set_options(self._html_page.get_elements_by_html_tag().keys(),
                                     self._html_page.get_css_class_names())
        css_code = self._css_fuzzer.fuzz()
        for canvas_id in self._html_page.get_elements_by_html_tag()['canvas']:
            self._canvas_fuzzer.set_canvas_id(canvas_id)
            self._js_functions.append("func_" + canvas_id)
            js_code += self._canvas_fuzzer.fuzz()
        js_code += self.__create_startup()
        for i in range(self._js_function_count):
            js_code += self.__build_function()
        return js_code, css_code

    def __create_startup(self):
        code = "function startup(){\n"
        for html_id in self._html_page.get_element_ids():
            var_name = "elem_" + str(len(self._js_objects['JS_DOM_ELEMENT']))
            element = self._html_page.get_element_by_id(html_id)
            code += "\t" + var_name + " = " + JsDocument.getElementById(html_id) + ";\n"
            self._js_objects['JS_DOM_ELEMENT'].append(JsDomElement(var_name, element['tag'], element['children']))
        for i in range(0, 10):
            code += self.__create_js_obj("JS_STRING")[0] + ";\n"
            code += self.__create_js_obj("JS_NUMBER")[0] + ";\n"
            code += self.__create_js_obj("JS_ARRAY")[0] + ";\n"
            code += self.__create_js_obj("JS_DOM_ELEMENT")[0] + ";\n"
        code += self.CALLING_BLOCK_COMMENT + "\n"
        code += "}\n"
        return code

    def __create_js_obj(self, js_obj_type):
        if js_obj_type == 'JS_STRING':
            js_string = JsString("str_" + str(len(self._js_objects[js_obj_type])))
            self._js_objects[js_obj_type].append(js_string)
            return js_string.newString(random.choice(FuzzValues.STRINGS)), js_string
        elif js_obj_type == 'JS_NUMBER':
            js_number = JsNumber("num_" + str(len(self._js_objects[js_obj_type])))
            self._js_objects[js_obj_type].append(js_number)
            return js_number.newNumber(random.choice(FuzzValues.INTS)), js_number
        elif js_obj_type == 'JS_ARRAY':
            js_array = JsArray("array_" + str(len(self._js_objects[js_obj_type])))
            self._js_objects[js_obj_type].append(js_array)
            array_content = []
            array_cont_type = random.choice(JS_OBJECTS)
            for i in range(0, 10):
                array_content.append(random.choice(self._js_objects[array_cont_type]))
            return js_array.newArray(array_content, array_cont_type), js_array
        elif js_obj_type == 'JS_DOM_ELEMENT':
            js_dom_element = JsDomElement("elem_" + str(len(self._js_objects[js_obj_type])), random.choice(HTML5_OBJECTS.keys()))
            self._js_objects[js_obj_type].append(js_dom_element)
            return js_dom_element.newElement(), js_dom_element

    def __build_function(self):
        tab = "\t"
        func_name = "func_" + str(len(self._js_functions))
        self._js_functions.append(func_name)
        code = "function " + func_name + "(){\n"
        for i in range(self._js_function_size):
            #  Assignment (<10), Method call (<20), Loop(<23), if cond(<26)
            selection = random.randint(0, 26)
            if selection < 20:
                code += tab + (self.__build_assignment() if selection < 15 else self.__build_method_call()) + ";\n"
                self._method_call_depth = 0
            elif selection < 23:
                code += tab + self.__build_loop()
            elif selection < 26:
                code += tab + self.__build_if_cond()
        code += "}\n"
        return code

    def __build_assignment(self):
        code = ""
        new_obj = random.randint(0, 10)
        obj_type = random.choice(JS_OBJECTS)
        if new_obj < 8:
            js_obj = random.choice(self._js_objects[obj_type])
        else:
            temp_code, js_obj = self.__create_js_obj(obj_type)
            code += temp_code + ";\n"
        code += js_obj.name + " = "
        code += self.__get_param(obj_type)
        if obj_type in VALID_OPERATORS.keys():
            for i in range(random.randint(1, 30)):
                operator = random.choice(VALID_OPERATORS[obj_type])
                code += operator + " " + self.__get_param(obj_type)
        code += ";\n"
        return code

    def __build_method_call(self, return_type=None):
        code = ""
        if return_type is None:
            js_obj = random.choice(self._js_objects['JS_DOM_ELEMENT'])
        else:
            obj_type = random.choice(RETURN_TYPES[return_type])
            js_obj = random.choice(self._js_objects[obj_type])
        print js_obj
        method = random.choice(js_obj.methods_and_properties_by_return_type[return_type])
        if method['parameters'] is not None:
            param_list = []
            for param in method['parameters']:
                param_list.append(self.__get_param(param))
            code += method['method'](*param_list)
        else:
            code += method['method']()
        return code

    def __build_loop(self):
        self._method_call_depth = 0  # after build assignment
        return "loop"

    def __build_if_cond(self):
        self._method_call_depth = 0  # after build assignment
        return "if"

    def __get_param(self, param_type):
        # TODO: decide if a constant value or a method call or an already existent value is chosen
        selection = random.randint(0, 10)
        code = ""
        # TODO: handle optional; catch non return types and just give them fixed val
        if param_type == 'JS_ARRAY_FUNCTION':
            pass
        else:
            if selection < 6:  # method
                if self._method_call_depth < 10:
                    self._method_call_depth += 1
                    code += self.__build_method_call(param_type)
                else:
                    code += self.__get_constant_param(param_type)
            elif selection < 8:  # constant
                code += self.__get_constant_param(param_type)
            else:  # existing element
                element = random.choice(self._js_objects[param_type])
                code += element.name
        return code

    def __get_constant_param(self, param_type):
        # TODO: CSS_CLASS; CSS_STYLE; JS_EVENT_LISTENER; HTML_ATTR; HTML_TAG; JS_DOM_CHILD_ELEMENT; ... check for more
        if param_type in self._html_fuzzer.TYPES_DICT:
            param = random.choice(self._html_fuzzer.TYPES_DICT[param_type])
            if param_type == 'JS_STRING':
                param = "\"" + param + "\""
            return param
        elif param_type == 'JS_ARRAY' or param_type == 'JS_DOM_ELEMENT':
            obj = random.choice(self._js_objects[param_type])
            return obj.name

