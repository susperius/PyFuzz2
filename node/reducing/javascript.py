from reducer import Reducer
import re
import logging
from fuzzing.browser.model.HtmlObjects import HTML5_OUTER_TAGS

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
        self._html_tag_list = []
        self._start = 0
        self._phase = 0
        self._try_start_pos = 0
        self._try_end_pos = 0
        self._html_pos = 0
        self._tag_removal_search_start_pos = 0
        self._removed_tag_pos = 0
        self._actual_tag_end = 0
        self._showed = False
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
        self._html_tag_list = self.__get_all_html_tags()
        self._start = 0
        self._phase = 0
        self._try_start_pos = 0
        self._try_end_pos = 0
        self._html_pos = 0
        self._tag_removal_search_start_pos = self._test_case.find("<br")


    @property
    def file_type(self):
        return self._file_type

    def crashed(self, crashed):
        if crashed:
            self._test_case = self._reduced_case
        if self._phase == 0 and len(self._functions) == 1:
            self._phase += 1
            self._showed = False
        elif self._phase == 1 and not self._event_handler:
            self._phase += 1
            self._showed = False
        elif self._phase == 2:
            if not crashed:
                self._start = self._try_end_pos
            self._try_start_pos = self._test_case.find("try{ ", self._start)
            if self._try_start_pos == -1:
                self._phase += 1
                self._showed = False
        elif self._phase == 3:
            if not crashed:
                self._tag_removal_search_start_pos = self._actual_tag_end
            else:
                self._tag_removal_search_start_pos = self._test_case.find("<br")
            if self._test_case.find("<", self._tag_removal_search_start_pos + 1) == -1:
                self._phase += 1

    def reduce(self):
        if self._phase == 0:
            if not self._showed:
                self._logger.info("Phase 0: JS FUNCTION REMOVING")
                self._showed = True
            function_name = self._functions.pop()
            self.__remove_function_call(function_name)
            self.__remove_function_body(function_name)
            print(self._functions)
        elif self._phase == 1:
            if not self._showed:
                self._logger.info("Phase 1: JS EVENT HANDLER REMOVING")
                self._showed = True
            self._reduced_case = self._test_case
            self.__remove_function_body(self._event_handler.pop())
        elif self._phase == 2:
            if not self._showed:
                self._logger.info("Phase 2: TRY-CATCH-BLOCK REMOVING")
                self._showed = True
            self.__remove_try_catch_block()
        elif self._phase == 3:
            if not self._showed:
                self._logger.info("Phase 3: HTML-TAGS REMOVING")
                self._showed = True
            self.__remove_html_tag()
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
        if function_call_start_pos != -1:
            function_call_line_start = self._test_case.rfind("\t", 0, function_call_start_pos)
            function_call_line_end = self._test_case.find(";\n", function_call_start_pos) + 2
            self._reduced_case = self._test_case[:function_call_line_start] + self._test_case[function_call_line_end:]

    def __remove_function_body(self, function_name):
        function_start_pos = self._reduced_case.find("function " + function_name)
        if function_start_pos != -1:
            function_end_pos = self._reduced_case.find("}\nfunction", function_start_pos) + 2
            self._reduced_case = self._reduced_case[:function_start_pos] + self._reduced_case[function_end_pos:]

    def __remove_try_catch_block(self):
        self._try_start_pos = self._test_case.find("try{ ", self._start)
        if self._try_start_pos == -1:
            self._reduced_case = None
        else:
            self._try_end_pos = self._test_case.find(" }\n", self._try_start_pos) + 3
            self._reduced_case = self._test_case[:self._try_start_pos] + self._test_case[self._try_end_pos:]

    def __remove_html_tag(self):
        ids = []  #  TODO: rethink all the tag finding stuff .... :/
        opening_tag_start, opening_tag_end, html_tag, id_value = self.__find_eligible_html_tag()
        while "foo" in html_tag:
            self._tag_removal_search_start_pos = self._actual_tag_end
            opening_tag_start, opening_tag_end, html_tag, id_value = self.__find_eligible_html_tag()
        ids.append(id_value)
        closing_tag_start = self._test_case.find("</" + html_tag, opening_tag_end)
        closing_tag_end = self._test_case.find(">", closing_tag_start)
        if html_tag in HTML5_OUTER_TAGS:
            # check html tag if it's a required outer tag and try to delete the whole block ...
            self._reduced_case = self._test_case[:opening_tag_start] + self._test_case[closing_tag_end + 1:]
            ids += self.__get_all_ids_in_block(self._test_case[opening_tag_end:closing_tag_start])
        elif closing_tag_start == -1:
            self._reduced_case = self._reduced_case[:opening_tag_start] + self._reduced_case[opening_tag_end + 1:]
        else:
            # just cut the html tag
            self._reduced_case = self._test_case[:closing_tag_start] + self._test_case[closing_tag_end + 1:]
            self._reduced_case = self._reduced_case[:opening_tag_start] + self._reduced_case[opening_tag_end + 1:]
        self.__remove_element_declarations(ids)

    def __remove_element_declarations(self, ids):
        for identifier in ids:
            declaration_start = self._reduced_case.find("elem_" + identifier)
            declaration_end = self._reduced_case.find(";", declaration_start)
            self._reduced_case = self._reduced_case[:declaration_start] + self._reduced_case[declaration_end + 1:]

    def __find_eligible_html_tag(self):
        opening_tag_start = self._test_case.find("<", self._tag_removal_search_start_pos + 1)
        opening_tag_end = self._test_case.find(">", opening_tag_start)
        self._actual_tag_end = opening_tag_end
        html_tag, id_value = self.__get_html_tag_info(self._test_case[opening_tag_start:opening_tag_end + 1])
        return opening_tag_start, opening_tag_end, html_tag, id_value

    @staticmethod
    def __get_html_tag_info(opening_tag):
        id_start_pos = opening_tag.find(" id")
        html_tag = opening_tag[1:id_start_pos]
        id_value_start = opening_tag.find("\"", id_start_pos)
        id_value_end = opening_tag.find("\"", id_value_start + 1)
        id_value = opening_tag[id_value_start + 1:id_value_end]
        return html_tag, id_value

    @staticmethod
    def __get_all_ids_in_block(code_block):
        ids = []
        id_start_pos = code_block.find(" id")
        id_value_start = code_block.find("\"", id_start_pos)
        id_value_end = code_block.find("\"", id_value_start + 1)
        while id_start_pos != -1:
            ids.append(code_block[id_value_start + 1:id_value_end])
            id_start_pos = code_block.find(" id", id_value_end)
            id_value_start = code_block.find("\"", id_start_pos)
            id_value_end = code_block.find("\"", id_value_start + 1)
        return ids

    def __remove_link_tag(self):
        link_tag_start = self._test_case.find("<link")
        link_tag_end = self._test_case.find(">", link_tag_start)
        self._reduced_case = self._test_case[link_tag_start:link_tag_end + 1]

    def test(self):
        return self.__get_all_html_tags()

    def __get_all_html_tags(self):
        not_usable_tags = ['html', 'head', 'title', 'script', 'body', 'foo', 'link', 'br']
        tag_list = []
        temp_tag_list = re.findall('<[a-z]+', self._test_case)
        for tag in temp_tag_list:
            tag_list.append(tag.replace("<", ""))
        for bad_tag in not_usable_tags:
            try:
                while True:
                    tag_list.remove(bad_tag)
            except Exception:
                pass
        return tag_list

