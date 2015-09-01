__author__ = 'martin'

JS_OBJECTS = ['String', 'Number', 'Date', 'Array', 'domElem']

class JsObject:
    CONSTRUCTOR = []

    def __init__(self, name, js_type, value):
        self._name = name
        self._type = js_type
        self._value = value

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value


class JsString(JsObject):

    def charAt(self, pos):
        return self._name + ".charAt(" + str(pos) + ")"

    def charCodeAt(self, pos):
        return self._name + ".charCodeAt(" + str(pos) + ")"

    def concat(self, string):
        return self._name + ".concat(\"" + string + "\")"

    def fromCharCode(self, unicode_value_list):
        ret = self._name + ".fromCharCode("
        for item in unicode_value_list:
            ret += str(item) + ", "
        ret = ret[:-1] + ")"
        return ret

    def indexOf(self, string):
        return self._name + ".indexOf(\"" + string + "\")"

    def lastIndexOf(self, string):
        return self._name + ".lastIndexOf(\"" + string + "\")"

    def localeCompare(self, string):
        return self._name + ".localeCompare(\"" + string + "\")"

    def match(self, string):
        return self._name + ".match(\"" + string + "\")"  # needs regex

    def replace(self, search_str, replace_str):
        return self._name + ".replace(\"" + search_str + "\", \"" + replace_str + "\")"

    def search(self, string):
        return self._name + ".search(\"" + string + "\")"

    def slice(self, string):
        return self._name + ".slice(\"" + string + "\")"

    def split(self, string):
        return self._name + ".split(\"" + string + "\")"

    def substr(self, start_pos, count):
        return self._name + ".substr(" + str(start_pos) + ", " + str(count) + ")"

    def substring(self, start_pos, count):
        return self._name + ".substring(" + str(start_pos) + ", " + str(count) + ")"

    def toLocaleLowerCase(self):
        return self._name + ".toLocaleLowerCase()"

    def toLocaleUpperCase(self):
        return self._name + ".toLocaleUpperCase()"

    def toLowerCase(self):
        return self._name + ".toLowerCase()"

    def toUpperCase(self):
        return self._name + ".toUpperCase()"

    def toString(self):
        return self._name + ".toString()"

    def trim(self):
        return self._name + ".trim()"

    def valueOf(self):
        return self._name + ".valueOf()"

class JsNumber(JsObject):

    def toExponential(self, number):
        return self._name + ".toExponential(" + str(number) + ")"

    def toFixed(self, number):
        return self._name + ".toFixed(" + str(number) + ")"

    def toPrecision(self, number):
        return self._name + ".toPrecision(" + str(number) + ")"

    def toString(self):
        return self._name + ".toString()"

    def valueOf(self):
        return self._name + ".valueOf()"

class JsDate(JsObject):

    def newDate(self, value):
        return "think about"

    def getDate(self):
        return self._name + ".getDate()"

    def getDay(self):
        return self._name + ".getDay()"

    def getFullYear(self):
        return self._name + ".getFullYear()"

    def getHours(self):
        return self._name + ".getHours()"

    def getMilliseconds(self):
        return self._name + ".getMilliseconds()"

    def getMinutes(self):
        return self._name + ".getMinutes()"

#  Go on ....