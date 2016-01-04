__author__ = 'susperius'

class JsWindow:

    @staticmethod
    def setTimeout(function, timeout):
        return "window.setTimeout(function () { " + function + " }, " + str(timeout) + ");"
