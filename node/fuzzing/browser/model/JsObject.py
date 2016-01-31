__author__ = 'susperius'

JS_OBJECTS = ['JsString', 'JsNumber', 'JsDate', 'JsArray', 'JsElement']


class JsObject:
    TYPE = "JsObject"

    def __init__(self, name):
        self._name = name
        self._basic_methods = {'toString': {'ret_val': 'STRING', 'parameters': None, 'method': self.toString}}

    @property
    def name(self):
        return self._name

    @property
    def methods_and_properties(self):
        raise NotImplementedError("ABSTRACT PROPERTY")

    def toString(self):
        return self._name + ".toString()"


class JsString(JsObject):
    TYPE = "JsString"

    @property
    def methods_and_properties(self):
        js_string_methods = {'charAt': {'ret_val': 'STRING', 'parameters': ['INT'], 'method': self.charAt},
                             'charCodeAt': {'ret_val': 'INT', 'parameters': ['INT'], 'method': self.charCodeAt},
                             'concat': {'ret_val': 'STRING', 'parameters': ['STRING'], 'method': self.concat},
                             'fromCharCode': {'ret_val': 'STRING', 'parameters': ['UNICODE_VALUE_LIST'], 'method': self.fromCharCode},
                             'indexOf': {'ret_val': 'INT', 'parameters': ['STRING'], 'method': self.indexOf},
                             'lastIndexOf': {'ret_val': 'INT', 'parameters': ['STRING'], 'method': self.lastIndexOf},
                             'localeCompare': {'ret_val': 'INT', 'parameters': ['STRING'], 'method': self.localeCompare},
                             'match': {'ret_val': 'STRING', 'parameters': ['REGEX'], 'method': self.match},
                             'replace': {'ret_val': 'STRING' ,'parameters': ['STRING', 'STRING'], 'method': self.replace},
                             'slice': {'ret_val': 'STRING','parameters': ['INT', 'INT'], 'method': self.slice},
                             'split': {'ret_val': 'STRING', 'parameters': ['STRING'], 'method': self.split},
                             'substr': {'ret_val': 'STRING', 'parameters': ['INT', 'INT'], 'method': self.substr},
                             'substring': {'ret_val': 'STRING', 'parameters': ['INT', 'INT'], 'method': self.substring},
                             'toLocaleLowerCase': {'ret_val': 'STRING', 'parameters': None, 'method': self.toLocaleLowerCase},
                             'toLowerCase': {'ret_val': 'STRING', 'parameters': None, 'method': self.toLowerCase},
                             'toLocaleUpperCase': {'ret_val': 'STRING', 'parameters': None, 'method': self.toLocaleUpperCase},
                             'toUpperCase': {'ret_val': 'STRING', 'parameters': None, 'method': self.toUpperCase},
                             'trim': {'ret_val': 'STRING', 'parameters': None, 'method': self.trim},
                             'valueOf': {'ret_val': 'STRING', 'parameters': None, 'method': self.valueOf},
                             'length': {'ret_val': 'INT', 'parameters': None, 'method': self.length}
                             }
        return js_string_methods.update(self._basic_methods)

    def charAt(self, pos):
        return self._name + ".charAt(" + str(pos) + ")"

    def charCodeAt(self, pos):
        return self._name + ".charCodeAt(" + str(pos) + ")"

    def concat(self, string):
        return self._name + ".concat(\"" + string + "\")"

    def fromCharCode(self, unicode_value):
        ret = self._name + ".fromCharCode("
        for item in unicode_value:
            ret += str(item) + ", "
        ret = ret[:-1] + ")"
        return ret

    def indexOf(self, string):
        return self._name + ".indexOf(\"" + string + "\")"

    def lastIndexOf(self, string):
        return self._name + ".lastIndexOf(\"" + string + "\")"

    def localeCompare(self, string):
        return self._name + ".localeCompare(\"" + string + "\")"

    def match(self, regex_str):
        return self._name + ".match(\"" + regex_str + "\")"  # needs regex

    def replace(self, search_str, replace_str):
        return self._name + ".replace(\"" + search_str + "\", \"" + replace_str + "\")"

    def search(self, string):
        return self._name + ".search(\"" + string + "\")"

    def slice(self, start_pos, end_pos):
        return self._name + ".slice(\"" + str(start_pos) + "," + str(end_pos) + "\")"

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

    def trim(self):
        return self._name + ".trim()"

    def valueOf(self):
        return self._name + ".valueOf()"

    def length(self):
        return self._name + ".length"


class JsNumber(JsObject):
    TYPE = "JsNumber"

    @property
    def methods_and_properties(self):
        js_number_methods = {'toExponential': {'ret_val': 'EXP_FLOAT', 'parameters': ['NUMBER'], 'methods': self.toExponential},
                             'toFixed': {'ret_val': 'STRING', 'parameters': ['INT'], 'methods': self.toFixed},
                             'toPrecision': {'ret_val': 'FLOAT', 'parameters': ['INT'], 'methods': self.toPrecision},
                             'valueOf': {'ret_val': 'INT', 'parameters': None, 'methods': self.valueOf}
                             }
        return js_number_methods.update(self._basic_methods)

    def toExponential(self, number):
        return self._name + ".toExponential(" + str(number) + ")"

    def toFixed(self, number):
        return self._name + ".toFixed(" + str(number) + ")"

    def toPrecision(self, number):
        return self._name + ".toPrecision(" + str(number) + ")"

    def valueOf(self):
        return self._name + ".valueOf()"

    # TODO: Add properties


class JsArray(JsObject):
    TYPE = "JsArray"

    def __init__(self, name):
        JsObject.__init__(name)
        self._array_elements = {}

    @property
    def methods_and_properties(self):
        # concat js_array, every bool, filter js_array, indexOf int, join string, lastIndexOf int, map js_array,
        # pop array_element, push js_array, reverse js_array
        js_array_methods_and_properties = {}
        return js_array_methods_and_properties

    def newArray(self, element_dict):
        code = self._name + " = ["
        for key in element_dict.keyes():
            code += key + ","
            self._array_elements[key] = element_dict[key]
        code = code[:-1] + "];"
        return code

    def concat(self, js_array_id):
        return self._name + ".concat(" + js_array_id + ")"

    def every(self, function_name):
        return self._name + ".every(" + function_name + ")"

    def filter(self, function_name):
        return self._name + ".filter(" + function_name + ")"

    def indexOf(self, array_element):
        return self._name + ".indexOf(" + array_element + ")"

    def join(self):
        return self._name + ".join()"

    def lastIndexOf(self, array_element):
        return self._name + ".lastIndexOf(" + array_element + ")"

    def map(self, function_name):
        return self._name + ".map(" + function_name + ")"

    def pop(self):
        # remove the last element
        return self._name + ".pop()"

    def push(self, js_object):
        return self._name + ".push(" + js_object + ")"

    def reverse(self):
        return self._name + ".reverse()"

    def shift(self):
        # remove the first element
        return self._name + ".shift()"


class JsDate(JsObject):
    TYPE = "JsDate"

    @property
    def methods_and_properties(self):
        js_data_methods_and_properties = {}  # TODO: Write down the stuff
        return js_data_methods_and_properties

    def newDate(self, value):
        return "new Date()"

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

    def getMonth(self):
        return self._name + ".getMonth()"

    def getSeconds(self):
        return self._name + ".getSeconds()"

#  Go on ....