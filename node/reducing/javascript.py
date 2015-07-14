__author__ = 'susperius'
from reducer import Reducer
import re
from fuzzing.jsfuzzer.browserObjects import Window


class JsReducer(Reducer):
    def __init__(self, test_case, program_path):
        self._test_case = test_case
        self._reduced_case = ""
        self._program_path = program_path
        self._functions = self.__find_functions()
        self._start = 0
        self._crashed = False
        self._phase = 0

    def crashed(self, crashed):
        self._crashed = crashed
        if self._crashed:
            self._test_case = self._reduced_case
        else:
            if self._phase == 0:
                if self._start + 2 < len(self._functions):
                    self._start += 1
                else:
                    self._phase = 1

    def reduce(self):
        if self._phase == 0:
            self.__remove_functions(self._start, self._start + 2)
        return self._reduced_case

    def __find_functions(self):
        func_list = ['function startup']
        func_list += re.findall('function func[0-9]+', self._test_case)
        func_list.append('function event_firing')
        return func_list

    def __remove_functions(self, start, end):
        start_pos = self._test_case.find(self._functions[start])
        end_func = self._functions[end].replace('function ', '')
        end_func_pos = self._test_case.find(self._functions[end])
        window_start_pos = self._test_case.find('window.setTimeout(', start_pos)
        window_end_pos = self._test_case.find(';', window_start_pos)
        self._reduced_case = self._test_case[:window_start_pos] + Window.setTimeout(end_func, 40) + + "\n}\n" + \
                             self._test_case[end_func_pos:]
