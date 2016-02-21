__author__ = 'susperius'


class JsGlobal:
    BOOL_OPERATORS = ['==', '===', '!=', '!==', '<', '>', '<=', '>=']

    @staticmethod
    def value_infinity():
        return "Infinity"

    @staticmethod
    def value_nan():
        return "NaN"

    @staticmethod
    def value_undefined():
        return "undefined"

    @staticmethod
    def func_decode_uri(uri):
        return "decodeURI("+uri+");"

    @staticmethod
    def func_encode_uri(uri):
        return "encodeURI("+uri+");"

    @staticmethod
    def func_decode_uri_component(uri):
        return "decodeURIComponent("+uri+");"

    @staticmethod
    def func_encode_uri_component(uri):
        return "encodeURIComponent("+uri+");"

    @staticmethod
    def func_eval(js_code):
        return "eval("+js_code+");"

    @staticmethod
    def func_is_finite(number):
        return "isFinite("+number+");"

    @staticmethod
    def func_is_nan(value):
        return "isNaN("+value+");"

    @staticmethod
    def func_number(obj_val):
        return "Number("+obj_val+");"

    @staticmethod
    def parse_float(float_string):
        return "parseFloat("+float_string+");"

    @staticmethod
    def parse_int(int_string):
        return "parseInt("+int_string+");"

    @staticmethod
    def string(obj_val):
        return "String("+obj_val+");"
    
    @staticmethod
    def try_catch_block(try_code, exception_code="ex", catch_code=""):
        return "try{ " + try_code + " } catch(" + exception_code + ") { " + catch_code + " }\n"
