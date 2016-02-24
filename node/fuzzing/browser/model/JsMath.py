class JsMath:

    def __init__(self):
        raise NotImplementedError("THIS CLASS IS A COLLECTION OF STATIC METHODS!")

    @staticmethod
    def E():
        return "Math.E"

    @staticmethod
    def LN2():
        return "Math.LN2"

    @staticmethod
    def LN10():
        return "Math.LN10"

    @staticmethod
    def LOG2E():
        return "Math.LOG2E"

    @staticmethod
    def LOG10E():
        return "Math.LOG10E"

    @staticmethod
    def PI():
        return "Math.PI"

    @staticmethod
    def SQRT1_2():
        return "Math.SQRT1_2"

    @staticmethod
    def SQRT2():
        return "Math.SQRT2"

    @staticmethod
    def abs(x):
        return "Math.abs(" + str(x) + ")"

    @staticmethod
    def acos(x):
        return "Math.acos(" + str(x) + ")"

    @staticmethod
    def asin(x):
        return "Math.asin(" + str(x) + ")"

    @staticmethod
    def atan(x):
        return "Math.atan(" + str(x) + ")"

    @staticmethod
    def atan2(x, y):
        return "Math.atan2(" + str(x) + ", " + str(y) + ")"

    @staticmethod
    def ceil(x):
        return "Math.ceil(" + str(x) + ")"

    @staticmethod
    def cos(x):
        return "Math.cos(" + str(x) + ")"

    @staticmethod
    def exp(x):
        return "Math.exp(" + str(x) + ")"

    @staticmethod
    def floor(x):
        return "Math.floor(" + str(x) + ")"

    @staticmethod
    def log(x):
        return "Math.log(" + str(x) + ")"

    @staticmethod
    def max(val_list):
        code = "Math.max("
        for x in val_list:
            code += str(x) + ", "
        code = code[:-2] + ")"
        return code

    @staticmethod
    def min(val_list):
        code = "Math.min("
        for x in val_list:
            code += str(x) + ", "
        code = code[:-2] + ")"
        return code

    @staticmethod
    def pow(x, y):
        return "Math.pow(" + str(x) + ", " + str(y) + ")"

    @staticmethod
    def random():
        return "Math.random()"

    @staticmethod
    def round(x):
        return "Math.round(" + str(x) + ")"

    @staticmethod
    def sin(x):
        return "Math.sin(" + str(x) + ")"

    @staticmethod
    def sqrt(x):
        return "Math.sqrt(" + str(x) + ")"

    @staticmethod
    def tan(x):
        return "Math.tan(" + str(x) + ")"

JS_MATH_METHODS = {
    'E': {'parameters': None, 'method': JsMath.E},
    'LN2': {'parameters': None, 'method': JsMath.LN2},
    'LN10': {'parameters': None, 'method': JsMath.LN10},
    'LOG2E': {'parameters': None, 'method': JsMath.LOG2E},
    'LOG10E': {'parameters': None, 'method': JsMath.LOG10E},
    'PI': {'parameters': None, 'method': JsMath.PI},
    'SQRT1_2': {'parameters': None, 'method': JsMath.SQRT1_2},
    'SQRT2': {'parameters': None, 'method': JsMath.SQRT2},
    'abs': {'parameters': ['INT'], 'method': JsMath.abs},
    'acos': {'parameters': ['INT'], 'method': JsMath.acos},
    'asin': {'parameters': ['INT'], 'method': JsMath.asin},
    'atan': {'parameters': ['INT'], 'method': JsMath.atan},
    'atan2': {'parameters': ['INT', 'INT'], 'method': JsMath.atan2},
    'ceil': {'parameters': ['INT'], 'method': JsMath.ceil},
    'cos': {'parameters': ['INT'], 'method': JsMath.cos},
    'exp': {'parameters': ['INT'], 'method': JsMath.exp},
    'floor': {'parameters': ['INT'], 'method': JsMath.floor},
    'log': {'parameters': ['INT'], 'method': JsMath.log},
    'max': {'parameters': ['INT'], 'method': JsMath.max},
    'min': {'parameters': ['INT'], 'method': JsMath.min},
    'pow': {'parameters': ['INT'], 'method': JsMath.pow},
    #'random': {'parameters': None, 'method': JsMath.random},
    'round': {'parameters': ['INT'], 'method': JsMath.round},
    'sin': {'parameters': ['INT'], 'method': JsMath.sin},
    'sqrt': {'parameters': ['INT'], 'method': JsMath.sqrt},
    'tan': {'parameters': ['INT'], 'method': JsMath.tan}
    }
