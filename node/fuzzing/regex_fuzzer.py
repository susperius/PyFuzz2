import random
import string
from fuzzer import Fuzzer
from browser.model.values import FuzzValues


class RegExFuzzer(Fuzzer):
    REGEX_FLAGS = ['g', 'i', 'm', 'y', '']
    REGEX_CHARACTER_CLASSES = ['.', '\\d', '\\D', '\\w', '\\W', '\\s', '\\S', '\\t', '\\r', '\\n',
                               '\\v', '\\f', '[\\b]', '\\0', '\\cX', '\\xHH', '\\uHHHH', '\\']
    REGEX_CHARACTER_SELECTION = ['[X]', '[^X]']
    REGEX_AREA_LIMITER = ['^', '$', '\\b', '\\B']
    REGEX_GROUPING_AND_REVERSE_REFERENCE = ['(X)', '\\N', '(?:X)']
    REGEX_QUANTIFIERS = ['*', '+', '*?', '+?', '?', 'X(?=Y)', 'X(?!Y)', 'X|Y', '{N}', '{N,}', '{N,M}']

    def __init__(self, max_length):
        self._max_length = max_length
        self._actual_length = 0
        self._component_to_method_mapping = {'char_classes': self.__get_character_class,
                                             'char_selection': self.__get_character_selector,
                                             'area_limiter': self.__get_area_limiter,
                                             'grouping_n_reverse': self.__get_reference,
                                             'quantifiers': self.__get_quantifier}

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
        pattern = ""
        while len(pattern) < int(self._max_length * 0.5):
            pattern += random.choice(FuzzValues.STRINGS)
        while len(pattern) < self._max_length:
            next_type = random.choice(self._component_to_method_mapping.items())
            pattern = next_type[1](pattern)
        regex += pattern
        regex += "/"
        regex += random.choice(self.REGEX_FLAGS)
        return regex

    @property
    def file_type(self):
        return None

    def __get_character_class(self, pattern):
        position = random.randint(0, int(len(pattern) * 0.75))
        char_class = random.choice(self.REGEX_CHARACTER_CLASSES)
        if char_class == "\\xHH":
            value = random.randint(0, 0xFF)
            if value < 0x10:
                hex_str = hex(value).replace("0x", "0")
            else:
                hex_str = hex(value).replace("0x", "")
            return pattern[:position] + "\\x" + hex_str + pattern[position+1:]
        elif char_class == "\\uHHHH":
            value = random.randint(0, 0xFFFF)
            if value < 0x10:
                hex_str = hex(value).replace("0x", "000")
            elif value < 0x100:
                hex_str = hex(value).replace("0x", "00")
            elif value < 0x1000:
                hex_str = hex(value).replace("0x", "0")
            else:
                hex_str = hex(value).replace("0x", "")
            return pattern[:position] + "\\u" + hex_str + pattern[position+1:]
        elif char_class == "\\cX":
            return pattern[:position] + "\\c" + random.choice(string.uppercase) + pattern[position+1:]
        else:
            return pattern[:position] + char_class + pattern[position+1:]

    def __get_character_selector(self, pattern):
        selector = random.choice(self.REGEX_CHARACTER_SELECTION)
        start = random.randint(0, int(len(pattern) * 0.75))
        end = random.randint(start + 1, len(pattern) - 1) # circumvent start > end scenarios
        if selector == "[X]":
            pattern = pattern[0:start] + "[" + pattern[start + 1:end] + "]" + pattern[end:]
        else:
            pattern = pattern[0:start] + "[^" + pattern[start + 1:end] + "]" + pattern[end:]
        return pattern

    def __get_area_limiter(self, pattern):
        limiter = random.choice(self.REGEX_AREA_LIMITER)
        position = random.randint(0, len(pattern) - 1)
        return pattern[:position] + limiter + pattern[position+1:]

    def __get_reference(self, pattern):
        reference = random.choice(self.REGEX_GROUPING_AND_REVERSE_REFERENCE)
        if reference == "\\N":
            number = random.randint(0, int(len(pattern) * 0.5))
            postition = random.randint(0, int(len(pattern) * 0.75))
            return pattern[:postition] + "\\" + str(number) + pattern[postition+1:]
        else:
            start = random.randint(0, int(len(pattern) * 0.75))
            end = random.randint(start, len(pattern) - 1)  # circumvent start > end scenarios
            if reference == "(X)":
                return pattern[:start] + "(" + pattern[start+1:end] + ")" + pattern[end+1:]
            else:
                return pattern[:start] + "(?:" + pattern[start + 1:end] + ")" + pattern[end + 1:]

    def __get_quantifier(self, pattern):
        quantifier = random.choice(self.REGEX_QUANTIFIERS)
        if "X" in quantifier:
            x = random.choice(FuzzValues.STRINGS)
            y = random.choice(FuzzValues.STRINGS)
            position = random.randint(0, len(pattern) - 1)
            if quantifier == "X(?=Y)":
                return pattern[:position] + " " + x + "(?=" + y + " " + pattern[position+1:]
            elif quantifier == "X(?!Y)":
                return pattern[:position] + " " + x + "(?!" + y + " " + pattern[position + 1:]
            else:
                return pattern[:position] + " " + x + "|" + y + " " + pattern[position + 1:]

        elif "N" in quantifier:
            position = random.randint(0, int(len(pattern) * 0.75))
            n = random.randint(0, int(len(pattern) * 0.75))
            if quantifier == "{N}":
                return pattern[:position] + "{" + str(n) + "}" + pattern[position+1:]
            elif quantifier == "{N,}":
                return pattern[:position] + "{" + str(n) + ",}" + pattern[position + 1:]
            else:
                m = random.randint(0, int(len(pattern) * 0.75))
                return pattern[:position] + "{" + str(n) + "," + str(m) + "}" + pattern[position + 1:]
        else:
            position = random.randint(0, int(len(pattern) * 0.75))
            return pattern[:position] + quantifier + pattern[position+1:]

