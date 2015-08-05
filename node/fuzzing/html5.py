__author__ = 'susperius'


import random
from jsfuzzer.values import FuzzValues


class Html5Fuzzer:
    TYPES_DICT = {'APP_DATA': None, 'BOOL': FuzzValues.BOOL, 'BUTTON_TYPE': FuzzValues.BUTTON_TYPE,
                  'CHAR': FuzzValues.CHARS, 'CHARACTER_SET': FuzzValues.CHARACTER_SET, 'COORDS': None, 'CSS': None,
                  'CSS_CLASS': None, 'DATETIME': None, 'DIRECTION': FuzzValues.TEXT_DIRECTION,
                  'ELEM_ID' : None, 'FORM_ID': None, 'FORM_METHOD': '', 'FORM_TARGET': '', 'FORM_ENCTYPE': '',
                  'HEADERS_ID': '', 'HTML_CODE': '', 'HTTP_EQUIV': '', 'INT': '', 'ID': '', 'LANG': '',
                  'MAP_NAME': '', 'MEDIA_TYPE': '', 'MEDIA_QUERY': '', 'MENU': '', 'METADATA_NAME': '',
                  'ONOFF': FuzzValues.ONOFF, 'PIXELS': '', 'PRELOAD': '', 'REL': '', 'SCROLLING': '', 'SHAPE': '', 'SANDBOX': '', 'SORTED': '',
                  'STRING': FuzzValues.STRINGS, 'TABLE_SCOPE': '', 'TARGET': '', 'TRACK_KIND': '', 'URL': '', 'WRAP': ''}

    def __init__(self, seed):
        if int(seed) == 0:
            random.seed()
        else:
            random.seed(int(seed))
        self._css_classes = []
        self._elem_id = []
        self._form_id = []


    def __get_app_data(self):
        return "data-" + random.choice(FuzzValues.STRINGS)

    def __get_coords(self):
        if random.choice([1, 2]) == 1:
            return random.choice(FuzzValues.INTS) + "," + random.choice(FuzzValues.INTS) + "," + \
                   random.choice(FuzzValues.INTS)
        else:
            return random.choice(FuzzValues.INTS) + "," + random.choice(FuzzValues.INTS) + "," + \
                   random.choice(FuzzValues.INTS) + "," + random.choice(FuzzValues.INTS)

    def __get_style(self):
        count = random.randint(1, 10)
        ret_val = ""
        for i in range(count):
            style_pick = random.choice(FuzzValues.CSS_STYLES)
            value = random.choice(style_pick[1:])
            ret_val += style_pick[0] + ":" + value + ";"
        return ret_val

    def __add_css_class(self):
        self._css_classes.append("style_class" + str(len(self._css_classes)))

    def __get_datetime(self):
        return str(random.randint(0, 9999)) + "-" + str(random.randint(0, 99)) + "-" + str(random.randint(0, 99)) + \
               " " + str(random.randint(0, 99)) + ":" + str(random.randint(0, 99))

    def __get_elem_id(self):
        return random.choice(self._elem_id)

    def __get_form_id(self):
        retrun random.choice(self._form_id)