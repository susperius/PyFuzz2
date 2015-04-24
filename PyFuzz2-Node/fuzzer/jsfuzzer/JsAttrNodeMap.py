# coding=utf8

class JsAttribute:
    def __init__(self, name):
        self.__name = name

    def prop_isId(self):
        return self.__name + ".isId"

    def prop_name(self):
        return self.__name + ".name"

    def prop_value(self):
        return self.__name + ".value"

    def prop_specified(self):
        return self.__name + ".specified"


class JsNamedNodeMap:
    def __init__(self, name):
        self.__name = name

    def getNamedItem(self, item_name):
        return self.__name + ".getNamedItem('" + item_name + "');\n"

    def item(self, index):
        return self.__name + ".item(" + index + ");\n"

    def removeNamedItem(self, item_name):
        return self.__name + ".removeItemName('" + item_name + "');\n"

    def setNamedItem(self, attr):
        return self.__name + ".setNamedItem(" + attr + ");\n"

    def prop_length(self):
        return self.__name + ".length"

