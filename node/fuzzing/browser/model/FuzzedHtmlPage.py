from HtmlObjects import HTML5_OBJECTS


class HtmlPage:
    def __init__(self):
        self._elements = {}
        self._raw_html = ""

    def set_raw_html(self, html):
        self._raw_html = html

    def get_raw_html(self):
        return self._raw_html

    def add_element(self, element_id, element_type):
        self._elements[element_id] = element_type

    def get_elements_by_id(self):
        return self._elements

    def get_elements_by_type(self):
        elements_by_type = dict.fromkeys(HTML5_OBJECTS.keys())
        for element_id in self._elements.iterkeys():
            if elements_by_type[self._elements[element_id]] is None:
                elements_by_type[self._elements[element_id]] = [element_id]
            else:
                elements_by_type[self._elements[element_id]].append(element_id)
        return elements_by_type

