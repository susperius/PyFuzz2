__author__ = 'susperius'


class WebSite:
    def __init__(self):
        self._funcs = ['home', 'node_detail']
        self._statuses = {200: '200 OK', 404: '404 FILE NOT FOUND'}
        self._standard_headers = [('Content-Type', 'text/html')]

    @property
    def funcs(self):
        return self._funcs

    def home(self):
        home_html = ['<b>Hello Home!</b>']
        return self._statuses[200], self._standard_headers, home_html

    def node_detail(self):
        node_detail_html = ['<b>Hello Node Detail!</b>']
        return self._statuses[200], self._standard_headers, node_detail_html

    def file_not_found(self):
        return self._statuses[404], self._standard_headers, ['<b>404 FILE NOT FOUND!</b>\n']
