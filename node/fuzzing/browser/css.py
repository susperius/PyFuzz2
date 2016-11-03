import random
from ..fuzzer import Fuzzer
from model.values import FuzzValues
from model.CssProperties import CSS_STYLES, CSS_SELECTOR_ELEMENT_CONJUNCTIONS, CSS_SELECTOR_STATIC_MODIFIERS
from html5 import Html5Fuzzer
#  TODO: Make it pretty and functional as fuzzer


class CssFuzzer(Fuzzer):
    NAME = "CssFuzzer"
    CONFIG_PARAMS = []

    def __init__(self):
        self._tags = []
        self._class_names = []
        self._attribs = []
        self._element_ids = []

    def set_tags(self, tags):
        self._tags = tags

    def set_class_names(self, class_names):
        self._class_names = class_names

    def set_options(self, tags, class_names, attribs, element_ids):
        self._tags = tags
        self._class_names = class_names
        self._attribs = attribs
        self._element_ids = element_ids

    @classmethod
    def from_list(cls, params):
        return CssFuzzer()

    def create_testcases(self, count, directory):
        pass  # TODO: implement

    def fuzz(self):
        style = ""
        for tag in self._tags:
            style += self.__create_style(tag)
        for class_name in self._class_names:
            style += self.__create_style("." + class_name)
        return style

    def __create_style(self, css_selector):
        style = css_selector + "{\n"
        for i in range(random.randint(5, 100)):
            style += "\t" + self.__create_style_statement() + "\n"
        style += "}\n"
        return style

    def __create_style_statement(self):
        prop = random.choice(CSS_STYLES)
        val = random.choice(prop[1:])
        return prop[0] + " : " + val + ";"

    def file_type(self):
        return "css"

    def __get_basic_css_selector(self):
        choice = random.randint(1,10)
        if choice < 3:
            return "*"
        elif choice < 7:
            return "." + random.choice(self._class_names)
        else:
            return "#" + random.choice(self._element_ids)

    def __get_linked_element_css_selector(self):
        choice = random.randint(1, 6)
        if choice == 1:
            return random.choice(self._tags)
        else:
            return random.choice(self._tags) + random.choice(CSS_SELECTOR_ELEMENT_CONJUNCTIONS) + \
                   random.choice(self._tags)

    def __get_attribute_css_selector(self):
        choice = random.randint(1, 7)
        attr = random.choice(list(self._attribs))
        if attr in Html5Fuzzer.TYPES_DICT.keys():
            if Html5Fuzzer.TYPES_DICT[attr] is not None:
                value = random.choice(Html5Fuzzer.TYPES_DICT[attr])
            else:
                value = random.choice(FuzzValues.STRINGS)
        else:
            value = random.choice(FuzzValues.STRINGS)
        if choice == 1:
            return "[" + attr + "]"
        elif choice == 2:
            return "[" + attr + "=" + value + "]"
        elif choice == 3:
            return "[" + attr + "~=" + value + "]"
        elif choice == 4:
            return "[" + attr + "|=" + value + "]"
        elif choice == 5:
            return "[" + attr + "^=" + value + "]"
        elif choice == 6:
            return "[" + attr + "$=" + value + "]"
        elif choice == 7:
            return "[" + attr + "*=" + value + "]"

    def __get_modifier_css_selector(self):
        choice = random.randint(1, 36)
        element = random.choice(self._tags + [""])  # tags and empty for all
        if choice == 1:
            return element + ":lang(" + random.choice(FuzzValues.LANG_CODES) + ")"
        elif choice == 2:
            return element + ":not(" + random.choice(self._tags) + ")"
        elif choice == 3:
            return element + ":nth-child(" + random.choice(FuzzValues.INTS) + ")"
        elif choice == 4:
            return element + ":nth-last-child(" + random.choice(FuzzValues.INTS) + ")"
        elif choice == 5:
            return element + ":nth-last-of-type(" + random.choice(FuzzValues.INTS) + ")"
        elif choice == 6:
            return element + ":nth-of-type(" + random.choice(FuzzValues.INTS) + ")"
        else:
            return element + random.choice(CSS_SELECTOR_STATIC_MODIFIERS)

    def get_css_selector(self):
        choice = random.randint(0, 11)
        if choice < 2:
            return self.__get_basic_css_selector()
        elif choice < 7:
            return self.__get_linked_element_css_selector()
        elif choice < 9:
            return self.__get_attribute_css_selector()
        elif choice <= 10:
            return self.__get_modifier_css_selector()
        elif choice == 11:
            return self.get_css_selector() + random.choice(CSS_SELECTOR_ELEMENT_CONJUNCTIONS) + self.get_css_selector()

