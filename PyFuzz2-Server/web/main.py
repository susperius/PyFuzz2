__author__ = 'susperius'


class WebSite:
    def __init__(self):
        self._funcs = ['home', 'node_detail']
        self._statuses = {200: '200 OK', 404: '404 FILE NOT FOUND'}
        self._header_html = [('Content-Type', 'text/html')]
        self._header_css = [('Content-Type', 'text/css')]

    @property
    def funcs(self):
        return self._funcs

    def home(self):
        with open("web/index.html", 'r') as fd:
            home_html = fd.read()
        home_html = home_html.replace("SECTION_TITLE", "OVERVIEW")
        home_html = home_html.replace("REPLACE_ME", "<b>Hello World</b>")
        return self._statuses[200], self._header_html, home_html

    def node_detail(self):
        node_detail_html = ['<b>Hello Node Detail!</b>']
        return self._statuses[200], self._header_html, node_detail_html

    def file_not_found(self):
        return self._statuses[404], self._header_html, ['<b>404 FILE NOT FOUND!</b>\n']

    def get_style(self):
        with open("web/style.css", 'r') as fd:
            style_css = fd.read()
        return self._statuses[200], self._header_css, style_css
