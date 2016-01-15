from HtmlObjects import HtmlObjects.HTML5_OBJECTS

class HtmlPage:
    def __init__(self):
        self._elements = {}
        self._raw_html = ""

    def add_element(self, element_id, element_type):
        self._elements[element_id] = element_type

    def set_raw_html(self, html):
        self._raw_html = html

    def get_elements_by_id(self):
        return self._elements

    def get_elements_by_type(self):
        elements_by_type = dict.fromkeys(HtmlObjects.)