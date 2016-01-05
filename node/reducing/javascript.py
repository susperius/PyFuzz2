__author__ = 'susperius'
from reducer import Reducer
import re
from fuzzing.browser.jsfuzzer.browserObjects import Window
import logging


class JsReducer(Reducer):
    NAME = 'js_reducer'
    CONFIG_PARAMS = ['file_type']

    def __init__(self, file_type):
        self._logger = logging.getLogger(__name__)
        self._file_type = file_type
        self._reduced_case = ""
        self._test_case = ""
        self._crash_report = ""
        self._functions = []
        self._event_handler = []
        self._start = 0
        self._crashed = False
        self._phase = 0
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

    def set_case(self, path, test_case, crash_report):
        with open(path + test_case, 'rb') as case_fd, open(path + crash_report, 'rb') as report_fd:
            self._test_case = case_fd.read()
            self._crash_report = report_fd.read()
            self._reduced_case = ""
            self._functions = self.__find_functions()
            self._event_handler = self.__find_event_handler()
            self._start = 0
            self._crashed = False
            self._phase = 0

    @property
    def file_type(self):
        return self._file_type

    @property
    def crash_report(self):
        return self._crash_report

    def crashed(self, crashed):
        self._crashed = crashed
        if self._crashed:
            self._test_case = self._reduced_case
            if self._phase == 0:
                self._functions = self.__find_functions()
                if self._start + 3 >= len(self._functions):
                    self._phase = 1
            elif self._phase == 1:
                self._event_handler = self.__find_event_handler()
                if self._start >= len(self._event_handler):
                    self._phase = 2
                    self._start = len(self._test_case)
        else:
            if self._phase == 0:
                if self._start + 3 < len(self._functions):
                    self._start += 1
                else:
                    self._phase = 1
                    self._start = 0
            elif self._phase == 1:
                self._start += 1
                if self._start >= len(self._event_handler):
                    self._phase = 2
                    self._start = len(self._test_case)
            elif self._phase == 2:
                try_pos, end_pos = self.__find_try_catch(self._start)
                self._start = try_pos

    def reduce(self):
        if self._phase == 0:
            self.__remove_functions(self._start, self._start + 2)
        elif self._phase == 1:
            self.__remove_event_handler(self._start)
        elif self._phase == 2:
            self.__remove_try_catch_block(self._start)
        else:
            return None
        return self._reduced_case

    def __find_functions(self):
        func_list = ['function startup']
        func_list += re.findall('function func[0-9]+', self._test_case)
        func_list.append('function event_firing')
        return func_list

    def __find_event_handler(self):
        func_list = re.findall('function [a-zA-Z]+_handler', self._test_case)
        return func_list

    def __remove_event_handler(self, handler_number):
        self._logger.debug('remove: ' + self._event_handler[handler_number])
        start_pos = self._test_case.find(self._event_handler[handler_number])
        end_pos = self._test_case.find(self._event_handler[handler_number + 1]) if handler_number + 1 < len(
            self._event_handler) else self._test_case.find('</script') - 1
        self._reduced_case = self._test_case[:start_pos] + self._test_case[end_pos:]

    def __remove_functions(self, start, end):
        self._logger.debug('remove: ' + self._functions[start + 1])
        start_pos = self._test_case.find(self._functions[start])
        end_func = self._functions[end].replace('function ', '')
        end_func_pos = self._test_case.find(self._functions[end])
        window_start_pos = self._test_case.find('window.setTimeout(', start_pos)
        self._reduced_case = self._test_case[:window_start_pos] + Window.setTimeout(end_func + '()', 40) + "\n}\n" + \
                             self._test_case[end_func_pos:]

    def __find_try_catch(self, start):
        try_pos = self._test_case.rfind('try{ ', 0, start)
        end_pos = self._test_case.find(' }\n', try_pos)
        end_pos += 3
        return try_pos, end_pos

    def __remove_try_catch_block(self, start):
        try_pos, end_pos = self.__find_try_catch(start)
        self._logger.debug('removing try-catch-block at position ' + str(try_pos))
        if try_pos == -1:
            self._phase = 3
            self._reduced_case = None
        else:
            self._reduced_case = self._test_case[:try_pos] + self._test_case[end_pos:]
