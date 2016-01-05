__author__ = 'susperius'


class Reducer:
    NAME = []
    CONFIG_PARAMS = []

    @classmethod
    def from_list(cls, params):
        raise NotImplementedError('ABSTRACT CLASS')

    @property
    def file_type(self):
        raise NotImplementedError('ABSTRACT CLASS')

    @property
    def crash_report(self):
        raise NotImplementedError('ABSTRACT CLASS')

    def reduce(self):
        raise NotImplementedError('ABSTRACT METHOD')

    def set_case(self, path, test_case, crash_report):
        raise NotImplementedError('ABSTRACT CLASS')