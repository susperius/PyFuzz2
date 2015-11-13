from values import FuzzValues

__author__ = 'susperius'


class Canvas2d:
    PATTERN_TYPES = ['repeat', 'repeat-x', 'repeat-y', 'no-repeat']
    LINE_STYLES = ['butt', 'round', 'square']
    LINE_JOIN_TYPES = ['bevel', 'round', 'miter']

    def __init__(self, var_name):
        self._name = var_name
        self._ctx = ""
        self._has_active_path = False
        self._gradients = []
        self._patterns = []

    @property
    def name(self):
        return self._ctx

    @property
    def gradients(self):
        return self._gradients

    @property
    def patterns(self):
        return self._patterns

    @property
    def has_active_path(self):
        return self._has_active_path

    def get_context(self, ctx_name):
        self._ctx = ctx_name
        return self.__allocation(self._ctx, self._name + ".getContext(\"2d\")")

    def fill_style(self, color):
        return self.__allocation(self._ctx + ".fillStyle", color, True)

    def stroke_style(self, color):
        return self.__allocation(self._ctx + ".strokeStyle", color, True)

    def shadow_color(self, color):
        return self.__allocation(self._ctx + ".shadowColor", color, True)

    def shadow_blur(self, number):
        return self.__allocation(self._ctx + ".shadowBlur", number)

    def shadow_offset_x(self, offset_x):
        return self.__allocation(self._ctx + ".shadowOffsetX", offset_x)

    def shadow_offset_y(self, offset_y):
        return self.__allocation(self._ctx + ".shadowOffsetY", offset_y)

    def create_linear_gradient(self, grd_name, x0, y0, x1, y1): #  Can be used as fillStyle !!
        self._gradients.append(grd_name)
        return "var " + grd_name + " = " + self._ctx + \
               ".createLinearGradient( " + str(x0) + ", " + str(y0) + ", " + str(x1) + ", " + str(y1) + ");\r\n"

    def create_pattern(self, pattern_name, patternable_obj, pattern_type):
        self._patterns.append(pattern_name)
        return "var " + pattern_name + " = " + self._ctx + ".createPattern(" + patternable_obj + ", \"" + patternable_obj + "\");\r\n"

    def line_cap(self, line_style):
        return self.__allocation(self._ctx + ".lineCap", line_style, True)

    def line_join(self, join_type):
        return self.__allocation(self._ctx + ".lineJoin", join_type, True)

    def line_width(self, width):
        return self.__allocation(self._ctx + ".lineWidth", width)

    def miterLimit(self, miter_length):
        return self.__allocation(self._ctx + ".miterLimit", miter_length)

    def rect(self, x, y, width, height):
        return self._ctx + ".rect(" + str(x) + ", " + str(y) + ", " + str(width) + ", " + str(height) + ");\r\n"

    def fill_rect(self, x, y, width, height):
        return self._ctx + ".fillRect(" + str(x) + ", " + str(y) + ", " + str(width) + ", " + str(height) + ");\r\n"

    def stroke_rect(self, x, y, width, height):
        return self._ctx + ".strokeRect(" + str(x) + ", " + str(y) + ", " + str(width) + ", " + str(height) + ");\r\n"

    def clear_rect(self, x, y, width, height):
        return self._ctx + ".clearRect(" + str(x) + ", " + str(y) + ", " + str(width) + ", " + str(height) + ");\r\n"

    def clip(self):
        return self._ctx + ".clip();\r\n"

    # ------------------------------------------------------------------------------------------------------
    # Path Methods CHECK FOR ACTIVE PATH!
    # ------------------------------------------------------------------------------------------------------
    def begin_path(self):
        self._has_active_path = True
        return self._ctx + ".beginPath();\r\n"

    def stroke(self):
        return self._ctx + ".stroke();\r\n"

    def fill(self):
        return self._ctx + ".fill();\r\n"

    def move_to(self, x, y):
        return self._ctx + ".moveTo(" + str(x) + ", " + str(y) + ");\r\n"

    def close_path(self):
        self._has_active_path = False
        return self._ctx + ".closePath();\r\n"

    def line_to(self, x, y):
        return self._ctx + ".lineTo(" + str(x) + ", " + str(y) + ");\r\n"

    def quadratic_curve_to(self, cpx, cpy, x, y):
        return self._ctx + ".quadraticCurveTo(" + str(cpx) + ", " + str(cpy) + "," + str(x) + ", " + str(y) + ");\r\n"

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        return self._ctx + ".bezierCurveTo(" + str(cp1x) + ", " + str(cp1y) + "," + str(cp2x) + ", " + str(cp2y) + "," + str(x) + ", " + str(y) + ");\r\n"

    def arc(self, x, y, r, start_angle, end_angle, counterclockwise):
        return self._ctx + "arc(" + str(x) + ", " + str(y) + ", " + str(r) + ", " + str(start_angle) + ", " + str(end_angle), ", " + str(counterclockwise) + ");\r\n"

    def arc_to(self, x0, y0, x1, y1, r):
        return self._ctx + ".arcTo(" + str(x0) + ", " + str(y0) + "," + str(x1) + ", " + str(y1) + ", " + str(r) + ");\r\n"

    # ATTENTION --->>>> NO SEMICOLON NOR NEWLINE!
    def is_point_in_path(self, x, y):
        return self._ctx + ".isPointInPath(" + str(x) + ", " + str(y) + ")"
    # ------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------

    def scale(self, x, y):
        return self._ctx + ".scale(" + str(x) + ", " + str(y) + ");\r\n"

    def rotate(self, angle):
        return self._ctx + ".rotate(" + str(angle) + ");\r\n"

    def translate(self, x, y):
        return self._ctx + ".translate(" + str(x) + ", " + str(y) + ");\r\n"

    def transform(self, a ,b, c, d, e, f):
        return self._ctx + ".transform(" + str(a) + ", " + str(b) + ", " + str(c) + ", " + str(d) + ", " + str(e) + ", " + str(f) + ");\r\n"

    def set_trans_form(self, a, b, c, d, e, f):
        return self._ctx + ".setTransform(" + str(a) + ", " + str(b) + ", " + str(c) + ", " + str(d) + ", " + str(e) + ", " + str(f) + ");\r\n"

    @staticmethod
    def __allocation(left_of_eq, right_of_eq, quotes=False):
        return str(left_of_eq) + " = \"" + str(right_of_eq) + "\";\r\n" if quotes else str(left_of_eq) + " = " + str(right_of_eq) + ";\r\n"


class CanvasWebGl:
    def __init__(self):
        pass
