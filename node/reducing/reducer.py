__author__ = 'susperius'


class Reducer:
    NAME = []
    CONFIG_PARAMS = []

    @property
    def crash_report(self):
        raise NotImplementedError('ABSTRACT CLASS')

    def reduce(self):
        raise NotImplementedError('ABSTRACT METHOD')