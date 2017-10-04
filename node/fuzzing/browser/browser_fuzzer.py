import random
from os import urandom
from sys import maxint
from html5 import Html5Fuzzer
from canvas import CanvasFuzzer
from css import CssFuzzer
from ..fuzzer import Fuzzer
from ..regex_fuzzer import RegExFuzzer
from model.FuzzedHtmlPage import HtmlPage
from model.JsObject import *
from model.JsDocument import JsDocument
from model.JsDomElement import JsDomElement
from model.values import FuzzValues
from model.HtmlObjects import HTML5_OBJECTS
from model.DomObjectTypes import DomObjectTypes


class BrowserFuzzer(Fuzzer):
    NAME = "browser_fuzzer"
    CONFIG_PARAMS = ["html_elements", "max_html_depth", "max_html_attr",
                     "js_function_count", "js_function_size", "file_type"]
    CALLING_BLOCK_COMMENT = "//CALLFUNCTIONS"

    def __init__(self, html_elements, max_html_depth, max_html_attr, js_function_count, js_function_size, file_type):
        random.seed(urandom(8))
        self._html_fuzzer = Html5Fuzzer(int(html_elements), int(max_html_depth), int(max_html_attr), file_type)
        self._css_fuzzer = CssFuzzer()
        self._canvas_fuzzer = CanvasFuzzer(int(js_function_size) * 2)
        self._reg_ex_fuzzer = RegExFuzzer(20)
        self._js_function_count = int(js_function_count)
        self._js_function_size = int(js_function_size)
        self._html_page = HtmlPage()
        self._js_functions = []
        self._js_objects = {}
        self._file_type = file_type
        self._method_call_depth = 0
        self._js_event_listener = []
        self._in_operation = False
        self._no_more_listeners = False

    def __init_js_objects_dict(self):
        for obj_type in JS_OBJECTS:
            self._js_objects[obj_type] = []

    def __reinit(self):
        self._js_functions = []
        self._js_objects = {}
        self.__init_js_objects_dict()
        self._css_selector = []
        self._method_call_depth = 0
        self._js_event_listener = []
        self._in_operation = False
        self._no_more_listeners = False

    def set_seed(self, seed):
        pass

    def prng_state(self):
        pass

    @property
    def file_type(self):
        return self._file_type

    @staticmethod
    def clear_folder(folder):
        Fuzzer.clear_folder(folder)

    def create_testcases(self, count, directory):
        self.clear_folder(directory)
        for i in range(count):
            test_name = "/test" + str(i) if i > 9 else "/test0" + str(i)
            with open(directory + test_name + "." + self.file_type, 'wb+') as html_file, open(directory + test_name + ".css", 'wb+') as css_file:
                fuzz = self.fuzz()
                html = fuzz[0].replace("TESTCASE.css", test_name + ".css")
                html_file.write(html)
                css_file.write(fuzz[1])



    @classmethod
    def from_list(cls, params):
        return cls(params[0], params[1], params[2], params[3], params[4], params[5])

    def set_state(self, state):
        pass

    def fuzz(self):
        self.__reinit()
        js_code = ""
        self._html_page = self._html_fuzzer.fuzz()
        for canvas_id in self._html_page.get_elements_by_html_tag()['canvas']:
            self._canvas_fuzzer.set_canvas_id(canvas_id)
            js_code += self._canvas_fuzzer.fuzz()
            self._js_functions.append("func_" + canvas_id)
        self._css_fuzzer.set_options(self._html_page.get_elements_by_html_tag().keys(),
                                     self._html_page.get_css_class_names(),
                                     self._html_page.get_attribs(),
                                     self._html_page.get_element_ids())
        css_code = self._css_fuzzer.fuzz()
        js_code += self.__create_startup()
        for i in range(self._js_function_count):
            js_code += self.__build_function()
        self._no_more_listeners = True
        for name in self._js_event_listener:
            js_code += self.__build_function(name, event=True)
        calling_block = ""
        for name in self._js_functions:
            choice = random.randint(1, 10)
            if choice < 8:
                calling_block += "\t" + name + "();\n"
            else:
                calling_block += "\twindow.setTimeout(" + name + "(), 10);\n"
        calling_block += self.__fire_events()
        js_code = js_code.replace(self.CALLING_BLOCK_COMMENT, calling_block)
        whole_page = self._html_page.get_raw_html().replace("SCRIPT_BODY", js_code)
        return whole_page, css_code

    def __create_startup(self):
        code = "function startup(){\n"
        for html_id in self._html_page.get_element_ids():
            var_name = "elem_" + str(len(self._js_objects['JS_DOM_ELEMENT']))
            element = self._html_page.get_element_by_id(html_id)
            code += "\t" + var_name + " = " + JsDocument.getElementById(html_id) + ";\n"
            self._js_objects['JS_DOM_ELEMENT'].append(JsDomElement(var_name, element['tag'], element['children']))
        for i in range(0, 10):
            code += "\t" + self.__create_js_obj("JS_STRING")[0] + ";\n"
            code += "\t" + self.__create_js_obj("JS_NUMBER")[0] + ";\n"
            code += "\t" + self.__create_js_obj("JS_ARRAY")[0] + ";\n"
            code += "\t" + self.__create_js_obj("JS_DOM_ELEMENT")[0] + ";\n"
        code += self.CALLING_BLOCK_COMMENT + "\n"
        code += "}\n"
        return code

    def __create_js_obj(self, js_obj_type):
        if js_obj_type == 'JS_STRING':
            js_string = JsString("str_" + str(len(self._js_objects[js_obj_type])))
            self._js_objects[js_obj_type].append(js_string)
            return js_string.newString("\"" + random.choice(FuzzValues.STRINGS) + "\""), js_string
        elif js_obj_type == 'JS_NUMBER':
            js_number = JsNumber("num_" + str(len(self._js_objects[js_obj_type])))
            self._js_objects[js_obj_type].append(js_number)
            return js_number.newNumber(random.choice(FuzzValues.INTS)), js_number
        elif js_obj_type == 'JS_ARRAY':
            js_array = JsArray("array_" + str(len(self._js_objects[js_obj_type])))
            array_content = []
            array_cont_type = random.choice(JS_OBJECTS)
            if not self._js_objects[array_cont_type]:
                array_cont_type = random.choice(['JS_STRING', 'JS_NUMBER'])
            for i in range(0, 10):
                array_content.append(random.choice(self._js_objects[array_cont_type]))
            self._js_objects[js_obj_type].append(js_array)
            return js_array.newArray(array_content, array_cont_type), js_array
        elif js_obj_type == 'JS_DOM_ELEMENT':
            js_dom_element = JsDomElement("elem_" + str(len(self._js_objects[js_obj_type])), random.choice(HTML5_OBJECTS.keys()))
            self._js_objects[js_obj_type].append(js_dom_element)
            ret_val = (js_dom_element.newElement(), js_dom_element) # if random.randint(1, 10) < 6 else (js_dom_element.newBodyElement(), js_dom_element)
            return ret_val

    def __build_function(self, name=None, event=False):
        tab = "\t"
        i = 0
        if name is None:
            func_name = "func_" + str(len(self._js_functions))
            self._js_functions.append(func_name)
        else:
            func_name = name
        code = "function " + func_name + "(){\n" if not event else "function " + func_name + "(ev){\n"
        while i < self._js_function_size:
            #  Assignment (<10), Method call (<24), Loop(<27)
            selection = random.randint(0, 26)
            if selection < 25:
                code += tab + "try{ "
                code += (self.__build_assignment() if selection < 15 else self.__build_method_call()) + "; } catch(err) {}\n"
                self._method_call_depth = 0
            elif selection < 27:
                loop_code, length = self.__build_loop()
                code += tab + loop_code
                i += length
            if event:
                code += tab + "try{ " + self.__build_method_call(js_object=JsDomElement("ev.target")) + "; } catch(err) {}\n"
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
        code += self.__get_param(obj_type) if obj_type != 'JS_ARRAY' else (self.__get_param(obj_type)).name
        if obj_type in VALID_OPERATORS.keys():
            self._in_operation = True
            for i in range(random.randint(1, 30)):
                operator = random.choice(VALID_OPERATORS[obj_type])
                code += operator + " " + self.__get_param(obj_type)
            self._in_operation = False
        code += ";"
        return code

    def __build_method_call(self, return_type=None, js_object=None):
        code = ""
        if return_type is None and not js_object:
            js_obj = random.choice(self._js_objects['JS_DOM_ELEMENT'])
        elif return_type not in RETURN_TYPES.keys() and not js_object:
            return self.__get_constant_param(return_type)
        elif js_object is not None:
            js_obj = js_object
        else:
            return_type = return_type.replace("*", "") if "*" in return_type else return_type
            obj_type = random.choice(RETURN_TYPES[return_type])
            js_obj = random.choice(self._js_objects[obj_type])
        if return_type != 'JS_NUMBER':
            method = random.choice(js_obj.methods_and_properties_by_return_type[return_type])
        else:
            method = random.choice(js_obj.methods_and_properties_by_return_type[random.choice(JS_NUMBERS)])
        if method['parameters'] is not None:
            param_list = []
            for param_type in method['parameters']:
                parameter = self.__get_param(param_type)
                param_list.append(parameter)
            code += method['method'](*param_list)
        else:
            code += method['method']()
        return code

    def __build_event_listener(self):
        pass  # TODO: Create event listener
        code = ""

    def __build_loop(self):
        code = "for(i="
        direction = random.randint(1, 2)
        length = random.randint(5, 100)
        i = random.randint(0, 1000)
        i = i - length if direction == 1 else i + length
        code += str(i) + "; i"
        code += "<=" if direction == 1 else ">="
        code += str(length) + "; i"
        code += "++" if direction == 1 else "--"
        code += "){\n"
        body_length = random.randint(10, 30)
        i = 0
        while i < body_length:
            selection = random.randint(1, 20)
            code += "\t\t" + "try{ "
            code += self.__build_assignment() if selection < 15 else self.__build_method_call() + ";"
            code += " } catch(err) {}\n"
            self._method_call_depth = 0  # after build assignment
            i += 1
        code += "\t}\n"
        return code, i

    def __build_if_cond(self):
        self._method_call_depth = 0  # after build assignment
        return "if"

    def __get_param(self, param_type):
        # TODO: decide if a constant value or a method call or an already existent value is chosen
        selection = random.randint(1, 10)
        code = ""
        if "*" in param_type and self._in_operation:
            return None
        elif "*" in param_type:
            param_type = param_type.replace("*", "")
        # TODO: handle optional; catch non return types and just give them fixed val
        if param_type == 'JS_ARRAY_FUNCTION':
            pass
        elif param_type == 'JS_ARRAY':
            return random.choice(self._js_objects['JS_ARRAY'])
        else:
            if selection < 7 and param_type in RETURN_TYPES.keys():  # method
                if self._method_call_depth < 10:
                    self._method_call_depth += 1
                    code += self.__build_method_call(param_type)
                else:
                    code += self.__get_constant_param(param_type)
            elif selection < 8 and param_type in JS_OBJECTS:  # existing element
                element = random.choice(self._js_objects[param_type]) if param_type not in JS_NUMBERS else random.choice(self._js_objects['JS_NUMBER'])
                code += element.name
            else:  # constant
                code += self.__get_constant_param(param_type)
        return code

    def __get_constant_param(self, param_type):
        # TODO:  CSS_STYLE; JS_EVENT_LISTENER; HTML_ATTR; HTML_TAG; JS_DOM_CHILD_ELEMENT; ... check for more
        if param_type in self._html_fuzzer.TYPES_DICT:
            param = random.choice(self._html_fuzzer.TYPES_DICT[param_type])
            if param_type == 'JS_STRING':
                param = "\"" + param + "\""
            return param
        elif param_type == 'JS_ARRAY' or param_type == 'JS_DOM_ELEMENT':
            obj = random.choice(self._js_objects[param_type])
            return obj.name
        elif param_type == 'CSS_SELECTOR':
            return self._css_fuzzer.get_css_selector()
        elif param_type == 'CSS_CLASS':
            return random.choice(self._html_page.get_css_class_names())
        elif param_type == 'HTML_ATTR':
            return random.choice(self._html_page.get_attribs())
        elif param_type == 'HTML_ATTR_VAL':
            html_attr_val = "\"" + random.choice(FuzzValues.INTERESTING_VALUES) + "\""
            return html_attr_val  # TODO: make an attr test interesting value list
        elif param_type == 'JS_OBJECT':
            obj_type = random.choice(JS_OBJECTS)
            js_obj = random.choice(self._js_objects[obj_type])
            return random.choice(js_obj.name)
        elif param_type == 'JS_EVENT_LISTENER':
            choice = random.randint(1, 10)
            if choice < 5 and self._js_event_listener or self._no_more_listeners:
                return random.choice(self._js_event_listener)
            else:
                listener_name = "event_listener_" + str(len(self._js_event_listener))
                self._js_event_listener.append(listener_name)
                if len(self._js_event_listener) > 5:
                    self._no_more_listeners = True
                return listener_name
        elif param_type == 'EVENT':
            return random.choice(DomObjectTypes.DOM_EVENTS)
        elif param_type == 'JS_DOM_CHILD_ELEMENT':
            js_obj = random.choice(self._js_objects['JS_DOM_ELEMENT'])
            while not js_obj.get_children():
                js_obj = random.choice(self._js_objects['JS_DOM_ELEMENT'])
            return random.choice(js_obj.get_children())
        elif param_type == 'JS_NUMBER':
            choice = random.randint(1, 5)
            if choice == 1:  # INT
                return str(random.randint(-1 * maxint, maxint))
            elif choice == 2:  # FLOAT
                return str(random.randint(-1 * maxint, maxint) + random.random())
            elif choice == 3:  # EXP_FLOAT
                return str(random.randint(-32000, 32000) + random.random()) + "e" + random.choice(['+', '-']) + str(random.randint(1, 1000))
            elif choice == 4:  # JS_NUMBER
                js_num = random.choice(self._js_objects['JS_NUMBER'])
                return js_num.name
            elif choice == 5:  # JS_NUMBER CONSTANT
                return random.choice(JsNumber.NUMBER_CONSTANTS)
        elif param_type == 'UNICODE_VALUE_LIST':
            length = random.randint(1, 100)
            unicode_list_str = ""
            for i in range(0, length):
                unicode_list_str += str(random.randint(1, 65535))
            return unicode_list_str
        elif param_type == 'REGEX':
            return "[^abc]"
            # return self._reg_ex_fuzzer.fuzz()
        else:
            print(param_type)
            return ""

    def __fire_events(self):
        code = ""
        for dom_element in self._js_objects['JS_DOM_ELEMENT']:
            if len(dom_element.registered_events) != 0:
                for event in dom_element.registered_events.keys():
                    code += "\ttry{" + dom_element.get_event_trigger(event) + "}catch(err) {}\n"
        return code
