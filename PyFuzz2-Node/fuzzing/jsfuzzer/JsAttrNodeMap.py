# coding=utf8

class JsAttribute:
    def __init__(self, name):
        self.__name = name

    def prop_is_id(self):
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

    def get_named_item(self, item_name):
        return self.__name + ".getNamedItem('" + item_name + "');"

    def item(self, index):
        return self.__name + ".item(" + index + ");"

    def remove_named_item(self, item_name):
        return self.__name + ".removeItemName('" + item_name + "');"

    def set_named_item(self, attr):
        return self.__name + ".setNamedItem(" + attr + ");"

    def prop_length(self):
        return self.__name + ".length"

