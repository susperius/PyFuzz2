from HtmlObjects import HTML5_OBJECTS

# Perhaps I could keep track of script and css also in this class ...


class HtmlPage:
    def __init__(self):
        self._elements = {}
        self._raw_html = ""
        self._css_class_names = []

    def set_raw_html(self, html):
        self._raw_html = html

    def get_raw_html(self):
        return self._raw_html

    def add_element(self, element_id, html_tag):
        self._elements[element_id] = html_tag

    def get_elements_by_id(self):
        return self._elements

    def get_element_by_id(self, element_id):
        return self._elements[element_id]

    def change_element(self, element_id, element_type):
        self._elements[element_id] = element_type

    def get_elements_by_html_tag(self):
        elements_by_type = {}
        for element_id in self._elements.keys():
            if self._elements[element_id] in elements_by_type.keys():
                elements_by_type[self._elements[element_id]].append(element_id)
            else:
                elements_by_type[self._elements[element_id]] = [element_id]
        return elements_by_type

    def get_element_ids(self):
        return self._elements.keys()

    def add_css_class_name(self, name):
        self._css_class_names.append(name)

    def get_css_class_names(self):
        return self._css_class_names

