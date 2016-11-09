import re
from reducer import Reducer


'''
    Phases:
    1 - Try to remove functions
    2 - Remove lines inside of functions
    3 - Remove html
    4 - Remove css
'''


class BrowserTestcaseReducer(Reducer):
    NAME = "browser"
    CONFIG_PARAMS = ['file_type']

    def __init__(self, file_type):
        self._file_type = file_type
        self._html_file = ""
        self._js_functions = []
        self._js_event_listeners = []
        self._js_function_re = re.compile("function func_[0-9]+")
        self._js_event_listener_re = re.compile("function event_listener_[0-9]+")
        self._phase = 1
        self._test_html_file = ""
        self._block_quotient = 2
        self._tried_removal = []
        self._line_count = 0

    def crashed(self, crashed):
        if self._phase == 1:
            if crashed:
                if len(self._js_functions) == 2:
                    self._phase += 1
                    self.__init_phase_2()
                else:
                    self._html_file = self._test_html_file
                    self._tried_removal = []
                    self._block_quotient = 2

            else:
                self._test_html_file = self._html_file
                if len(self._tried_removal) == len(self._js_functions):
                    if len(self._js_functions) / self._block_quotient == 1:
                        self._phase += 1
                        self.__init_phase_2()
                    else:
                        self._block_quotient *= 2
                        self._tried_removal = []
        elif self._phase == 2:
            if crashed:
                self._html_file = self._test_html_file
                self._tried_removal = []
                self._block_quotient = 2
            else:
                self._test_html_file = self._html_file
                if self._line_count == len(self._tried_removal):
                    if self._line_count / self._block_quotient == 1:
                        if len(self._js_functions) > 1:
                            self._js_functions.pop(0)
                        else:
                            self._phase += 1
                    else:
                        self._block_quotient *= 2
                        self._tried_removal = []

    def __init_phase_2(self):
        self._js_functions = self._js_function_re.findall(self._html_file)
        self._block_quotient = 2
        self._tried_removal = []

    @classmethod
    def from_list(cls, params):
        return cls(params[0])

    @property
    def reduce_add_file(self):
        return False, None

    @property
    def file_type(self):
        return self._file_type

    def set_case(self, path, test_case):
        with open(path + test_case, 'rb') as fd:
            self._html_file = fd.read()
        self._test_html_file = self._html_file

    def reduce(self):
        print("Phase: " + str(self._phase))
        if self._phase == 1:
            self._js_functions = self._js_function_re.findall(self._html_file)
            print("Available Functions: " + str(self._js_functions))
            self._js_event_listeners = self._js_event_listener_re.findall(self._html_file)
            rem_func = []
            count = len(self._js_functions) / self._block_quotient
            for func in self._js_functions:
                if func not in self._tried_removal and count > 0:
                    self.__remove_js_function(func.replace("function ", ""))
                    count -= 1
                    self._tried_removal.append(func)
                    rem_func.append(func)
                elif count < 1:
                    break
            print("This time removed function: " + str(rem_func))
        elif self._phase == 2:
            func_name = self._js_functions[0].replace("function ", "")
            print("Function reduction: " + func_name)
            func_start_pos, func_end_pos = self.__find_function_pos(func_name)
            func_start_pos = self._test_html_file.find("\n", func_start_pos) + 1
            function_lines = self._test_html_file[func_start_pos:func_end_pos].splitlines(True)
            self._line_count = len(function_lines)
            count = self._line_count / self._block_quotient
            i = 0
            removed_lines = []
            for line in function_lines:
                if i not in self._tried_removal and count > 0:
                    function_lines.remove(line)
                    count -= 1
                    removed_lines.append(i)
                    self._tried_removal.append(i)
                elif count < 1:
                    break
                i += 1
            print("Removed line numbers: " + str(removed_lines))
            replace_str = ""
            for line in function_lines:
                replace_str += line
            self._test_html_file = self._test_html_file[:func_start_pos] + replace_str + self._test_html_file[func_end_pos:]
        else:
            return None
        return self._test_html_file

    def __find_function_pos(self, name):
        func_start_pos = self._test_html_file.find("function " + name)
        func_end_pos = self._test_html_file.find("\n}\n", func_start_pos)
        return func_start_pos, func_end_pos

    def __remove_js_function(self, name):
        call_start_pos = self._test_html_file.find(name + "();")
        if call_start_pos == -1:
            call_start_pos = self._test_html_file.find("window.setTimeout(" + name)
        call_end_pos = self._test_html_file.find(";", call_start_pos)
        self._test_html_file = self._test_html_file[0:call_start_pos] + self._test_html_file[call_end_pos + 3:]
        func_start_pos, func_end_pos = self.__find_function_pos(name)
        self._test_html_file = self._test_html_file[0:func_start_pos] + self._test_html_file[func_end_pos+3:]
