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
    def reduce_add_file(self):
        raise NotImplementedError('ABSTRACT CLASS')

    def reduce(self):
        raise NotImplementedError('ABSTRACT METHOD')

    def set_case(self, path, test_case):
        raise NotImplementedError('ABSTRACT CLASS')

    def crashed(self, crashed):
        raise NotImplementedError('ABSTRACT CLASS')