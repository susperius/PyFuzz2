__author__ = 'susperius'


import random
from jsfuzzer.htmlObjects import HtmlObjects
from jsfuzzer.values import FuzzValues
from fuzzer import Fuzzer


class Html5Fuzzer(Fuzzer):
    TYPES_DICT = {'APP_DATA': None, 'BOOL': FuzzValues.BOOL, 'BUTTON_TYPE': FuzzValues.BUTTON_TYPE,
                  'CHAR': FuzzValues.CHARS, 'CHARACTER_SET': FuzzValues.CHARACTER_SET, 'COORDS': None, 'CSS': None,
                  'CSS_CLASS': None, 'DATETIME': None, 'DIRECTION': FuzzValues.TEXT_DIRECTION,
                  'ELEM_ID' : None, 'FORM_ID': None, 'FORM_METHOD': FuzzValues.FORM_METHOD,
                  'FORM_TARGET': FuzzValues.FORM_TARGET, 'FORM_ENCTYPE': FuzzValues.FORM_ENCTYPE,
                  'HEADER_ID': None, 'HTML_CODE': None, 'HTTP_EQUIV': FuzzValues.HTTP_EQUIV, 'INT': FuzzValues.INTS,
                  'ID': None, 'LANG': FuzzValues.LANG_CODES, 'MAP_NAME': None, 'MEDIA_TYPE': FuzzValues.MEDIA_TYPE,
                  'MEDIA_QUERY': None, 'MENU': None, 'METADATA_NAME': FuzzValues.METADATA_NAME,
                  'ONOFF': FuzzValues.ONOFF, 'PIXELS': FuzzValues.INTS, 'PRELOAD': FuzzValues.PRELOAD,
                  'REL': FuzzValues.REL, 'SCROLLING': FuzzValues.SCROLLING, 'SHAPE': FuzzValues.SHAPE,
                  'SANDBOX': FuzzValues.SANDBOX, 'SORTED': FuzzValues.SORTED, 'STRING': FuzzValues.STRINGS,
                  'TABLE_SCOPE': FuzzValues.TABLE_SCOPE, 'TARGET': FuzzValues.TARGET,
                  'TRACK_KIND': FuzzValues.TRACK_KIND, 'URL': None, 'WRAP': FuzzValues.WRAP}

    #  Not supported by major browser: MEDIA_QUERY MENU

    def __init__(self, seed, elements, max_depth, max_attr, file_type):
        if int(seed) == 0:
            random.seed()
        else:
            random.seed(int(seed))
        self._css_classes = []
        self._elem_ids = []
        self._form_ids = []
        self._header_ids = []
        self._map_names = []
        self._file_type = file_type
        self._max_attr = int(max_attr)
        self._max_depth = int(max_depth)
        self._elements = int(elements)


    @classmethod
    def from_list(cls, params):
        pass

    def file_type(self):
        return self._file_type

    def set_seed(self, seed):
        random.seed(int(seed))

    def prng_state(self):
        return random.getstate()

    def set_state(self, state):
        random.setstate(state)

    def create_testcases(self, count, directory):
        pass

    def fuzz(self):
        head = ""
        body = ""
        return self.__build_tag()

    def __build_tag(self, tag=None):
        open_tag = ""
        close_tag = ""
        elem_id = "id" + str(len(self._elem_ids))
        tag = random.choice(HtmlObjects.HTML5_OBJECTS.keys()) if tag is None else tag
        close_tag += "</" + tag + ">"
        if HtmlObjects.HTML5_OBJECTS[tag]['outer_tag'] is not None:
            open_tag, close_tag_out = self.__build_tag(random.choice(HtmlObjects.HTML5_OBJECTS[tag]['outer_tag']))
            close_tag += close_tag_out
        open_tag += "<" + tag + " id=\"" + elem_id + "\""
        self._elem_ids.append(elem_id)
        if tag == "form":
            self._form_ids.append(elem_id)
        elif tag == "th":
            self._header_ids.append(elem_id)
        attribs_avail = HtmlObjects.HTML5_OBJECTS[tag]['attr']
        max_tag_attr = len(attribs_avail.keys())
        attr_count = random.randint(1, self._max_attr) if self._max_attr < max_tag_attr else \
            random.randint(1, max_tag_attr)
        attribs = set()
        if HtmlObjects.HTML5_OBJECTS[tag]['req_attr'] is not None:
            for attr in HtmlObjects.HTML5_OBJECTS[tag]['req_attr']:
                attribs.add(attr)
        while len(attribs) < attr_count:
            attribs.add(random.choice(attribs_avail.keys()))
        for attr in attribs:
            if attribs_avail[attr] is None:  # Attributes without value
                open_tag += " " + attr
            else:
                open_tag += " " + attr + "=\""
                if self.TYPES_DICT[attribs_avail[attr]] is not None:  # attributes with value from lists
                    if tag == 'map' and attr == 'name':
                        name = "map" + str(len(self._map_names))
                        self._map_names.append(name)
                        open_tag += name
                    else:
                        open_tag += random.choice(self.TYPES_DICT[attribs_avail[attr]])
                else:  # attributes with value from runtime sources
                    open_tag += self.__get_value(attribs_avail[attr])
                open_tag += "\""
        return open_tag, close_tag

    def __get_value(self, attr_type):  # TODO: Complete
        if attr_type == "APP_DATA":
            pass
        elif attr_type == "COORDS":
            return self.__get_coords()
        elif attr_type == "CSS":
            return self.__get_style()
        elif attr_type == "CSS_CLASS":
            pass
        elif attr_type == "DATETIME":
            return self.__get_datetime()
        elif attr_type == "ELEM_ID":
            return self.__get_elem_id()
        elif attr_type == "FORM_ID":
            return self.__get_form_id() if len(self._form_ids) > 0 else "none"
        elif attr_type == "URL":
            return "http://127.0.0.1:8080"
        return ""

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
        return random.choice(self._elem_ids)

    def __get_form_id(self):
        return random.choice(self._form_ids)

    def __get_header_id(self):
        return random.choice(self._header_ids)

    def __gen_html_code(self):  # TODO: Implement
        pass

    def __get_map_name(self):
        return random.choice(self._map_names)

    def __get_url(self, mediatype):
        pass