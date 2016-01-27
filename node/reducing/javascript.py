from reducer import Reducer
import re
import logging

__author__ = 'susperius'


class JsReducer(Reducer):
    NAME = 'js_reducer'
    CONFIG_PARAMS = ['file_type']

    def __init__(self, file_type):
        self._logger = logging.getLogger(__name__)
        self._file_type = file_type
        self._reduced_case = ""
        self._test_case = ""
        self._functions = []
        self._event_handler = []
        self._canvas_function = []
        self._start = 0
        self._phase = 0
        self._try_start_pos = 0
        self._try_end_pos = 0
        '''
        Phases in reducing:
        0 - Determine which functions are necessary
        1 - Determine which event handler are necessary
        2 - Determine which LOCs are necessary
        3 - Determine which html objects are necessary
        '''

    @classmethod
    def from_list(cls, params):
        return cls(params[0])

    def set_case(self, path, test_case):
        with open(path + test_case, 'rb') as case_fd:
            self._test_case = case_fd.read()
        self._test_case = self._test_case.replace("\r\n", "\n")
        self._reduced_case = ""
        self._functions = self.__get_functions()
        self._event_handler = self.__get_event_handler_functions()
        self._canvas_function = self.__get_canvas_functions()
        self._start = 0
        self._phase = 0
        self._try_start_pos = 0
        self._try_end_pos = 0

    @property
    def file_type(self):
        return self._file_type

    def crashed(self, crashed):
        if crashed:
            self._test_case = self._reduced_case
        if self._phase == 0 and len(self._functions) == 1:
            self._phase += 1
        elif self._phase == 1 and not self._event_handler:
            self._phase += 1
        elif self._phase == 2:
            if not crashed:
                self._start = self._try_end_pos

    def reduce(self):
        if self._phase == 0:
            self.__remove_function(self._functions.pop(0), self._functions[0])
        elif self._phase == 1:
            self.__remove_function(self._event_handler.pop(0))
        elif self._phase == 2:
            self.__remove_try_catch_block()
        return self._reduced_case

    def __get_functions(self):
        # func_list = ['function startup']
        func_list = []
        func_list += re.findall('function func[0-9]+', self._test_case)  # normal functions
        # func_list.append('function event_firing')
        return func_list

    def __get_event_handler_functions(self):
        func_list = re.findall('function [a-zA-Z]+_handler', self._test_case)
        return func_list

    def __get_canvas_functions(self):
        func_list = re.findall('function func_id[0-9]+', self._test_case)
        return func_list

    def __remove_function(self, function_name, next_function=None):
        self._logger.debug("Removing function: " + function_name)
        function_start_pos = self._test_case.find(function_name)
        function_end_pos = self._test_case.find("}\nfunction", function_start_pos) + 2
        self._reduced_case = self._test_case[:function_start_pos] + self._test_case[function_end_pos:]
        if next_function is not None:
            function_name = function_name.replace("function", "")
            next_function = next_function.replace("function", "")
            self._reduced_case = self._reduced_case.replace(
                    function_name + "() }, ",
                    next_function + "() }, "
            )

    def __remove_try_catch_block(self):
        self._try_start_pos = self._test_case.find("try{ ", self._start)
        if self._try_start_pos == -1:
            self._reduced_case = None
        else:
            self._try_end_pos = self._test_case.find(" }\n", self._try_start_pos) + 3
            self._reduced_case = self._test_case[:self._try_start_pos] + self._test_case[self._try_end_pos:]

