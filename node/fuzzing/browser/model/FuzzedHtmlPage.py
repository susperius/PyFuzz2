from HtmlObjects import HTML5_OBJECTS

# Perhaps I could keep track of script and css also in this class ...


class HtmlPage:
    def __init__(self):
        self._elements = {}
        self._raw_html = ""
        self._css_class_names = []
        self._elements_by_tag = {}
        self._attribs = set()

    def set_raw_html(self, html):
        self._raw_html = html

    def get_raw_html(self):
        return self._raw_html

    def add_element(self, element_id, html_tag):
        self._elements[element_id] = self.__new_element(html_tag)  # {'tag': html_tag, 'children': []}
        if html_tag in self._elements_by_tag.keys():
            self._elements_by_tag[html_tag].append(element_id)
        else:
            self._elements_by_tag[html_tag] = [element_id]

    def add_child_to_element(self, element_id, child_id):
        self._elements[element_id]['children'].append(child_id)

    def get_elements_by_id(self):
        return self._elements

    def get_element_by_id(self, element_id):
        return self._elements[element_id]

    def get_elements_by_html_tag(self):
        return self._elements_by_tag

    def get_element_ids(self):
        return self._elements.keys()

    def add_css_class_name(self, name):
        self._css_class_names.append(name)

    def get_css_class_names(self):
        return self._css_class_names

    def add_attrib(self, attr):
        self._attribs.add(attr)

    def get_attribs(self):
        return list(self._attribs)

    @staticmethod
    def __new_element(tag):
        return {'tag': tag, 'children': []}
