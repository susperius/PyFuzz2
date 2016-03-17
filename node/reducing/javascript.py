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
        self._html_pos = 0
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
        self._html_pos = 0

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
            function_name = self._functions.pop()
            self.__remove_function_call(function_name)
            self.__remove_function_body(function_name)
        elif self._phase == 1:
            self._reduced_case = self._test_case
            self.__remove_function_body(self._event_handler.pop())
        elif self._phase == 2:
            self.__remove_try_catch_block()
        return self._reduced_case

    def __get_functions(self):
        # func_list = ['function startup']
        func_list = set(re.findall('func_[0-9]+', self._test_case))  # normal functions
        # func_list.append('function event_firing')
        return func_list

    def __get_event_handler_functions(self):
        func_list = set(re.findall('[a-zA-Z]+_handler', self._test_case))
        return func_list

    def __get_canvas_functions(self):
        func_list = set(re.findall('func_id[0-9]+', self._test_case))
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

    def __remove_function_call(self, function_name):
        self._logger.info("Removing function: " + function_name)
        # First remove the function call
        function_call_start_pos = self._test_case.find(function_name)
        function_call_line_start = self._test_case.rfind("\t", 0, function_call_start_pos)
        function_call_line_end = self._test_case.find(";\n", function_call_start_pos) + 2
        self._reduced_case = self._test_case[:function_call_line_start] + self._test_case[function_call_line_end:]

    def __remove_function_body(self, function_name):
        function_start_pos = self._test_case.find("function " + function_name)
        function_end_pos = self._test_case.find("}\nfunction", function_start_pos) + 2
        self._reduced_case = self._reduced_case[:function_start_pos] + self._reduced_case[function_end_pos:]

    def __remove_try_catch_block(self):
        self._try_start_pos = self._test_case.find("try{ ", self._start)
        if self._try_start_pos == -1:
            self._reduced_case = None
        else:
            self._try_end_pos = self._test_case.find(" }\n", self._try_start_pos) + 3
            self._reduced_case = self._test_case[:self._try_start_pos] + self._test_case[self._try_end_pos:]

    def __remove_html_tag(self):
        body_start_pos = self._test_case.find("<body")
        body_end_pos = self._test_case.find("</body>")
        open_tag_start_pos = self._test_case.find("<", body_start_pos + 1, body_end_pos)
        open_tag_end_pos = self._test_case.find(">", open_tag_start_pos) + 1
        id_start = self._test_case.find(" id", open_tag_start_pos, open_tag_end_pos)
        html_tag = self._test_case[open_tag_start_pos + 1:id_start]
        close_tag_start_pos = self._test_case.find("</" + html_tag + ">")
        another_open_tag_pos = self._test_case.find(html_tag, open_tag_end_pos, close_tag_start_pos)
        while another_open_tag_pos != -1:  # Their might be another html tag opened which is closed by our found end tag
            old_close_tag_start_pos = close_tag_start_pos
            close_tag_start_pos = self._test_case.find("</" + html_tag + ">", old_close_tag_start_pos + 1)
            another_open_tag_pos = self._test_case.find(html_tag, old_close_tag_start_pos + 1, close_tag_start_pos)
        close_tag_end_pos = self._test_case.find(">", close_tag_start_pos) + 1
        # first remove the closing tag so the positions are not destroyed
        self._reduced_case = self._test_case[:close_tag_start_pos] + self._test_case[close_tag_end_pos:]
        self._reduced_case = self._reduced_case[:open_tag_start_pos] + self._reduced_case[open_tag_end_pos:]



