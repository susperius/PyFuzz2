import re
from reducer import Reducer


class CSSReducer(Reducer):
    NAME = "css_reducer"
    CONFIG_PARAMS = ['file_type', 'reduce_add_file']

    def __init__(self, file_type, reduce_add_file):
        self._file_type = file_type
        #self._reduce_add_file = True if "True" in reduce_add_file else False
        self._test_case = ""
        self._actual_pos = 0
        self._last_deleted = 0
        self._reduced_case = ""
        self._phase = 0
        self._css_sections = []

    @classmethod
    def from_list(cls, params):
        return cls(params[0], params[1])

    def set_case(self, path, test_case):
        test_case = test_case.replace(".html", ".css")
        with open(path + test_case, 'rb') as fd:
            self._test_case = fd.read()
        with open(path + "backup.css", 'wb+') as fd:
            fd.write(self._test_case)
        self._actual_pos = 0
        self._last_deleted = 0
        self._reduced_case = ""
        self._phase = 0
        self._css_sections = self.__get_all_css_sections()

    def crashed(self, crashed):
        if crashed:
            self._test_case = self._reduced_case
        if self._phase == 0:
            if not self._css_sections:
                self._phase += 1
        elif self._phase == 1:
            if not crashed:
                self._actual_pos = self._last_deleted
            if self._test_case.find("\t", self._actual_pos) == -1:
                self._phase += 1

    @property
    def file_type(self):
        return self._file_type

    @property
    def reduce_add_file(self):
        return True, "css"

    def reduce(self):
        if self._phase == 0:
            section_name = self._css_sections.pop(0)
            while not self.__delete_css_section(section_name):
                if self._css_sections:
                    section_name = self._css_sections.pop(0)
                else:
                    break
        elif self._phase == 1:
            line_start_pos = self._test_case.find("\t")
            if line_start_pos != -1:
                line_end_pos = self._test_case.find(";") + 2  # remove also the line feed
                self._reduced_case = self._test_case[:line_start_pos] + self._test_case[line_end_pos:]
                self._last_deleted = line_end_pos
            else:
                self._reduced_case = None
        else:
            self._reduced_case = None
        return self._reduced_case

    def __get_all_css_sections(self):
        css_sections = re.findall('[a-z\.]+', self._test_case)
        return css_sections

    def __delete_css_section(self, section_name):
        ret_val = False
        section_start_pos = self._test_case.find(section_name + "{")
        if section_start_pos != -1:
            section_end_pos = self._test_case.find("}", section_start_pos)
            self._reduced_case = self._test_case[:section_start_pos] + self._test_case[section_end_pos + 2:]
            ret_val = True
        return ret_val
