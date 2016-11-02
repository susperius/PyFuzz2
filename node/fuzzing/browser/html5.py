import random
import logging

from model.HtmlObjects import *
from model.values import FuzzValues
from model.CssProperties import CSS_STYLES
from ..fuzzer import Fuzzer
from model.FuzzedHtmlPage import HtmlPage


class Html5Fuzzer(Fuzzer):
    TYPES_DICT = {'APP_DATA': None, 'BOOL': FuzzValues.BOOL, 'BUTTON_TYPE': FuzzValues.BUTTON_TYPE,
                  'CHAR': FuzzValues.CHARS, 'CHARACTER_SET': FuzzValues.CHARACTER_SET,
                  'COORDS': None, 'CROSSORIGIN': 'TODO', 'CSS': None,
                  'CSS_CLASS': None, 'DATALIST_ID': None, 'DATETIME': None, 'TEXT_DIRECTION': FuzzValues.TEXT_DIRECTION,
                  'INPUT_TYPE': FuzzValues.INPUT_TYPES,
                  'ELEM_ID' : None, 'FORM_ID': None, 'FORM_METHOD': FuzzValues.FORM_METHOD,
                  'FORM_TARGET': FuzzValues.FORM_TARGET, 'FORM_ENCTYPE': FuzzValues.FORM_ENCTYPE,
                  'HEADER_ID': None, 'HTML_CODE': None, 'HTTP_EQUIV': FuzzValues.HTTP_EQUIV, 'INT': FuzzValues.INTS,
                  'ID': None, 'KEYTYPE': 'TODO',
                  'LANG': FuzzValues.LANG_CODES, 'MAP_NAME': None, 'MEDIA_TYPE': FuzzValues.MEDIA_TYPE,
                  'MEDIA_QUERY': None, 'MENU': None, 'METADATA_NAME': FuzzValues.METADATA_NAME,
                  'ONOFF': FuzzValues.ONOFF, 'PURE_INT': FuzzValues.PURE_INTS,
                  'PIXELS': FuzzValues.INTS, 'PRELOAD': FuzzValues.PRELOAD,
                  'REGEXP': None,
                  'REL': FuzzValues.REL, 'SCROLLING': FuzzValues.SCROLLING, 'SHAPE': FuzzValues.SHAPE,
                  'SANDBOX': FuzzValues.SANDBOX, 'SORTED': FuzzValues.SORTED, 'STRING': FuzzValues.STRINGS,
                  'JS_STRING': FuzzValues.STRINGS,  # TODO: avoid workaround
                  'SRC': None,
                  'TABLE_SCOPE': FuzzValues.TABLE_SCOPE, 'TARGET': FuzzValues.TARGET,
                  'TRACK_KIND': FuzzValues.TRACK_KIND, 'URL': None, 'WRAP': FuzzValues.WRAP,
                  'YESNO': FuzzValues.YESNO}

    #  Not supported by major browser: MEDIA_QUERY MENU
    #  TODO: DATALIST_ID, REGEXP, URL ... dl creation ...

    NO_SINGLE_USE_TAGS = ['head', 'body', 'th', 'tr', 'td', 'tfoot', 'tbody', 'thead', 'title', 'dt', 'dd']
    NO_CHILD_LIST = ['select', 'time', 'iframe', 'style', 'canvas']

    def __init__(self, elements, max_depth, max_attr, file_type):
        self._logger = logging.getLogger(__name__)
        self._css_classes = []
        self._elem_ids = []
        self._form_ids = []
        self._canvas_ids = []
        self._header_ids = []
        self._map_names = []
        self._file_type = file_type
        self._embed_sources_list = []
        self._max_attr = int(max_attr)
        self._max_depth = int(max_depth)
        self._elements = int(elements)
        self._head = ""
        self._body = ""
        self._used_tags = set()
        self._html_page = HtmlPage()
        self._actual_elem_id = ""
        self._actual_parent_id = ""

    @classmethod
    def from_list(cls, params):
        pass  # TODO: implement

    @property
    def embed_sources_list(self):
        return self._embed_sources_list

    @embed_sources_list.setter
    def embed_sources_list(self, sources_list):
        self._embed_sources_list = sources_list

    def add_embed_source(self, item):
        self.embed_sources_list.append(item)

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

    def __reinit(self):
        self._head = ""
        self._body = ""
        self._elem_ids = []
        self._css_classes = []
        self._form_ids = []
        self._canvas_ids = []
        self._header_ids = []
        self._map_names = []
        self._used_tags = set()
        self._html_page = HtmlPage()

    def fuzz(self):
        self.__reinit()
        count = 0
        tag, self._head, close_head = self.__build_tag("head")
        head_id = self._actual_elem_id
        tag, title_open, title_close = self.__build_tag("title", ignore_outer_tag=True)
        self._html_page.add_child_to_element(head_id, self._actual_elem_id)
        self._head += title_open + random.choice(FuzzValues.STRINGS) + title_close + "\r\n"
        self._head += "<link rel=\"stylesheet\" href=\"TESTCASE.css\">\r\n"
        self._head += "<script type='text/javascript'>\r\nSCRIPT_BODY\r\n</script>\r\n"
        tag, self._body, close_body = self.__build_tag("body")
        body_id = self._actual_elem_id
        self._body = self._body[:-2] + " onload=\"eval(setTimeout(function () { startup(); }, 200))\">\r\n"
        self._body += "HELLO WORLD!\r\n<br>"
        while self._elements >= count:
            closing_list = []
            self._actual_parent_id = body_id
            for i in range(random.randint(1, self._max_depth)):
                tag, open_tag, close_tag = self.__build_tag()
                count += 1
                if HTML5_OBJECTS[tag]['outer_tag'] is not None\
                   and HTML5_OBJECTS[tag]['outer_tag'] == "head":  # Tags only allowed in head
                    self._head += open_tag + random.choice(FuzzValues.STRINGS) + close_tag + "\r\n"
                    self._html_page.add_child_to_element(head_id, self._actual_elem_id)
                else:  # default body tags
                    self._body += open_tag + random.choice(FuzzValues.STRINGS)
                    go_deeper = random.choice([0, 1])  # 0 = don't go deeper; 1 = go deeper
                    if go_deeper == 0 or tag in self.NO_CHILD_LIST:
                        self._html_page.add_child_to_element(self._actual_parent_id, self._actual_elem_id)
                        self._body += close_tag + "\r\n"
                    else:
                        self._html_page.add_child_to_element(self._actual_parent_id, self._actual_elem_id)
                        self._actual_parent_id = self._actual_elem_id
                        self._body += "\r\n"
                        closing_list.append(close_tag if tag != "br" else "")
            closing_list.reverse()
            for close_tag in closing_list:
                self._body += close_tag + "\r\n"
        if len(self._canvas_ids) == 0:
            tag, open_tag, close_tag = self.__build_tag('canvas')
            self._body += open_tag + close_tag + "\r\n"
        for source in self.embed_sources_list:
            self._body += "<embed src=\"" + source + "\">\r\n"
        html = "<!DOCTYPE html>\r\n<html>\r\n" + self._head + close_head + "\r\n" + self._body + close_body + "\r\n" + \
               "</html>\r\n"
        self._html_page.set_raw_html(html)
        return self._html_page

    def get_some_html_code(self, length):
        code = ""
        for i in range(length):
            tag = random.choice(HTML5_OBJECTS.keys())
            while HTML5_OBJECTS[tag]['outer_tag'] is not None:
                tag = random.choice(HTML5_OBJECTS.keys())
            tag, open_tag, close_tag = self.__build_tag(tag)
            code += open_tag + random.choice(FuzzValues.INTERESTING_VALUES) + close_tag + "\n"
        return code

    def __build_tag(self, tag=None, ignore_outer_tag=False):
        open_tag = ""
        close_tag = ""
        elem_id = "id" + str(len(self._elem_ids))
        if tag is None:
            tags = [x for x in HTML5_OBJECTS.keys() if x not in self.NO_SINGLE_USE_TAGS]
            tag = random.choice(tags)
            self._used_tags.add(tag)
            if tag == "table":
                # self._html_page.add_element(elem_id, tag)
                return "table", self.__build_table(), ""
            elif tag == "dl":
                # self._html_page.add_element(elem_id, tag)
                return "dl", self.__build_dl(), ""
        self._elem_ids.append(elem_id)
        self._html_page.add_element(elem_id, tag)
        self._actual_elem_id = elem_id
        if tag == "canvas":
            self._canvas_ids.append(elem_id)
        close_tag += "</" + tag + ">"
        if HTML5_OBJECTS[tag]['outer_tag'] is not None and not ignore_outer_tag:
            if "head" not in HTML5_OBJECTS[tag]['outer_tag']:
                ignore, open_tag, close_tag_out = self.__build_tag(random.choice(HTML5_OBJECTS[tag]['outer_tag']))
                close_tag += close_tag_out
        open_tag += "<" + tag + " id=\"" + elem_id + "\""
        if tag == "form":
            self._form_ids.append(elem_id)
        elif tag == "th":
            self._header_ids.append(elem_id)
        attribs_avail = HTML5_OBJECTS[tag]['attr']
        max_tag_attr = len(attribs_avail.keys())
        attr_count = random.randint(1, self._max_attr) if self._max_attr < max_tag_attr else \
            random.randint(1, max_tag_attr)
        attribs = set()
        if HTML5_OBJECTS[tag]['req_attr'] is not None:
            for attr in HTML5_OBJECTS[tag]['req_attr']:
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
        open_tag += "> "
        return tag, open_tag, close_tag

    def __build_table(self):
        table = ""
        parent_id = self._actual_parent_id
        tag, open_table, close_table = self.__build_tag("table", ignore_outer_tag=True)
        table_id = self._actual_elem_id
        self._html_page.add_child_to_element(parent_id, self._actual_elem_id)
        table += open_table + "\r\n"
        #  Table header
        tag, open_thead, close_thead = self.__build_tag("thead", ignore_outer_tag=True)
        self._html_page.add_child_to_element(table_id, self._actual_elem_id)
        parent_id = self._actual_elem_id
        table += open_thead + "\r\n"
        tag, open_tr, close_tr = self.__build_tag("tr", ignore_outer_tag=True)
        self._html_page.add_child_to_element(parent_id, self._actual_elem_id)
        parent_id = self._actual_elem_id
        table += open_tr + "\r\n"
        for i in range(random.randint(1, self._max_depth)):
            tag, open_th, close_th = self.__build_tag("th", ignore_outer_tag=True)
            self._html_page.add_child_to_element(parent_id, self._actual_elem_id)
            table += open_th +random.choice(FuzzValues.STRINGS) + close_th + "\r\n"
        table += close_tr + "\r\n" + close_thead + "\r\n"
        #  Table foot
        tag, open_tfoot, close_tfoot = self.__build_tag("tfoot", ignore_outer_tag=True)
        self._html_page.add_child_to_element(table_id, self._actual_elem_id)
        parent_id = self._actual_elem_id
        table += open_tfoot + "\r\n"
        tag, open_tr, close_tr = self.__build_tag("tr", ignore_outer_tag=True)
        self._html_page.add_child_to_element(parent_id, self._actual_elem_id)
        parent_id = self._actual_elem_id
        table += open_tr + "\r\n"
        for i in range(random.randint(1, self._max_depth)):
            tag, open_td, close_td = self.__build_tag("td", ignore_outer_tag=True)
            self._html_page.add_child_to_element(parent_id, self._actual_elem_id)
            table += open_td + random.choice(FuzzValues.STRINGS) + close_td + "\r\n"
        table += close_tr + "\r\n" + close_tfoot + "\r\n"
        #  Table body
        tag, open_tbody, close_tbody = self.__build_tag("tbody", ignore_outer_tag=True)
        self._html_page.add_child_to_element(table_id, self._actual_elem_id)
        parent_id = self._actual_elem_id
        table += open_tbody + "\r\n"
        for i in range(random.randint(1, self._max_depth)):
            tag, open_tr, close_tr = self.__build_tag("tr", ignore_outer_tag=True)
            self._html_page.add_child_to_element(parent_id, self._actual_elem_id)
            actual_tr = self._actual_elem_id
            table += open_tr + "\r\n"
            for i in range(random.randint(1, self._max_depth)):
                tag, open_td, close_td = self.__build_tag("td", ignore_outer_tag=True)
                self._html_page.add_child_to_element(actual_tr, self._actual_elem_id)
                table += open_td + random.choice(FuzzValues.STRINGS) + close_td + "\r\n"
            table += close_tr + "\r\n"
        table += close_tbody + "\r\n"
        table += close_table
        return table

    def __build_dl(self):
        return ""

    def __get_value(self, attr_type):  # TODO: Complete
        if attr_type == "APP_DATA":
            pass
        elif attr_type == "COORDS":
            return self.__get_coords()
        elif attr_type == "CSS":
            return self.__get_style()
        elif attr_type == "CSS_CLASS":
            self.__add_css_class()
            return random.choice(self._html_page.get_css_class_names())
        elif attr_type == "DATETIME":
            return self.__get_datetime()
        elif attr_type == "ELEM_ID":
            return self.__get_elem_id()
        elif attr_type == "FORM_ID":
            return self.__get_form_id() if len(self._form_ids) > 0 else "none"
        elif attr_type == "URL":
            return "http://127.0.0.1:8080"
        elif attr_type == "SRC":
            return self._embed_sources_list.pop() if self._embed_sources_list is not None and self._embed_sources_list else ""
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
        count = random.randint(2, 10)
        ret_val = ""
        for i in range(count):
            style_pick = random.choice(CSS_STYLES)
            value = random.choice(style_pick[1:])
            ret_val += style_pick[0] + ":" + value + ";"
        return ret_val

    def __add_css_class(self):
        class_name = "style_class_" + str(len(self._css_classes))
        self._html_page.add_css_class_name(class_name)
        return class_name

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