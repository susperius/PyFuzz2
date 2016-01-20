__author = "susperius"


class JsFunctions:
    def __init__(self, calling_comment):
        self._functions = {}

    def add_function(self, function_title, function_block, event_handler=False):
        self._functions[function_title] = {'raw_js': function_block, 'event_handle': event_handler}

    def get_function_titles(self):
        return self._functions.keys()

    def set_calling_block(self, function_title, calling_block):
        pass

    def get_whole_js(self):
        js = ""
        for function in self._functions.items():
            fs = function
        return js
