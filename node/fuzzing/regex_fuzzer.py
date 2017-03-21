import random
from fuzzer import Fuzzer
from browser.model.values import FuzzValues


class RegExFuzzer(Fuzzer):
    REGEX_FLAGS = ['g', 'i', 'm', 'y']
    REGEX_CHARACTER_CLASSES = ['.', '\\d', '\\D', '\\w', '\\W', '\\s', '\\S', '\\t', '\\r', '\\n',
                               '\\v', '\\f', '[\\b]', '\\0', '\\cX', '\\xHH', '\\uHHHH', '\\']
    REGEX_CHARACTER_SELECTION = ['[X]', '[^X]']
    REGEX_AREA_LIMITER = ['^', '$', '\\b', '\\B']
    REGEX_GROUPING_AND_REVERSE_REFERENCE = ['(X)', '\\N', '(?:X)']
    REGEX_QUANTORS = ['*', '+', '*?', '+?', '?', 'X(?=Y)', 'X(?!Y)', 'X|Y', '{N}', '{N,}', '{N,M}']

    REGEX_PATTERN_COMPONENTS = {'char_classes': REGEX_CHARACTER_CLASSES,
                                'char_selection': REGEX_CHARACTER_SELECTION,
                                'area_limiter': REGEX_AREA_LIMITER,
                                'grouping_n_reversing': REGEX_GROUPING_AND_REVERSE_REFERENCE,
                                'quantors': REGEX_QUANTORS}

    def __init__(self, max_length):
        self._max_length = max_length
        self._actual_length = 0

    @classmethod
    def from_list(cls, params):
        return cls(params[0])

    @staticmethod
    def clear_folder(folder):
        Fuzzer.clear_folder(folder)

    def create_testcases(self, count, directory):
        raise NotImplementedError("This Fuzzer does not support testfile generation")

    def fuzz(self):
        self._actual_length = 0
        regex = "/"
        pattern = random.choice(FuzzValues.STRINGS)

        regex += "/"

    @property
    def file_type(self):
        return None



