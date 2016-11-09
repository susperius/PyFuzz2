from reducer import Reducer


class BrowserTestcaseReducer(Reducer):
    def __init__(self, file_type):
        self._file_type = file_type

    def crashed(self, crashed):
        pass

    def reduce(self):
        pass

    @classmethod
    def from_list(cls, params):
        pass

    @property
    def reduce_add_file(self):
        return False, None

    @property
    def file_type(self):
        pass

    def set_case(self, path, test_case):
        pass