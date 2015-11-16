from values import FuzzValues

__author__ = 'susperius'


class Canvas2d:
    PATTERN_TYPES = ['repeat', 'repeat-x', 'repeat-y', 'no-repeat']
    LINE_STYLES = ['butt', 'round', 'square']
    LINE_JOIN_TYPES = ['bevel', 'round', 'miter']
    TEXT_ALIGNMENTS = ['start', 'end', 'center', 'left', 'right']
    TEXT_BASELINES = ['alphabetic', 'top', 'hanging', 'middle', 'ideographic', 'bottom']
    FONT_TYPES = ['20px Arial']

    def __init__(self, var_name):
        self._name = var_name
        self._ctx = ""
        self._has_active_path = False
        self._gradients = []
        self._patterns = []
        self._ints = range(0, 1024)
        self._attributes = {"fill_style": {"func": self.fill_style, "parameter": FuzzValues.COLORS + self.gradients},
                            "stroke_style": {"func": self.stroke_style, "parameter": FuzzValues.COLORS},
                            "shadow_color": {"func": self.shadow_color, "parameter": FuzzValues.COLORS},
                            "shadow_blur": {"func": self.shadow_blur, "parameter": self.ints},
                            "shadow_offset_x": {"func": self.shadow_offset_x, "parameter": self.ints},
                            "shadow_offset_y": {"func": self.shadow_offset_y, "parameter": self.ints},
                            "line_cap": {"func": self.line_cap, "parameter": Canvas2d.LINE_STYLES},
                            "line_join": {"func": self.line_join, "parameter": Canvas2d.LINE_JOIN_TYPES},
                            "line_width": {"func": self.line_width, "parameter": self.ints},
                            "miter_limit": {"func": self.miter_limit, "parameter": self.ints},
                            "font": {"func": self.font, "parameter": Canvas2d.FONT_TYPES},
                            "text_align": {"func": self.text_align, "parameter": Canvas2d.TEXT_ALIGNMENTS},
                            "text_baseline": {"func": self.text_baseline, "parameter": Canvas2d.TEXT_BASELINES}}
        # "begin_path" is not in the list because it is handled in the fuzzer to check for a active path
        self._path_methods = ["stroke", "fill", "move_to", "close_path", "line_to", "quadratic_curve_to",
                              "bezier_curve_to", "arc", "arc_to"]
        self._rect_methods = ["rect", "fill_rect", "stroke_rect", "clear_rect", "clip"]
        self._methods = ["create_linear_gradient", "create_pattern", "scale", "rotate", "translate", "transform",
                         "set_transform", "fill_text",
                         "stroke_text", "measure_text", "draw_image"] + self._path_methods + self._rect_methods



    # region PROPERTIES
    @property
    def name(self):
        return self._name

    @property
    def context(self):
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

    @property
    def attributes(self):
        return self._attributes

    @property
    def methods(self):
        return self._methods

    @property
    def path_methods(self):
        return self._path_methods

    @property
    def rect_methods(self):
        return self._rect_methods

    @property
    def ints(self):
        return self._ints
    # endregion

    def __add_int_var(self, var_name):
        self._ints.append(var_name)

    def __get_grad_name(self):
        return "gradient" + str(len(self._gradients))

    def __get_pattern_name(self):
        return "pattern" + str(len(self._patterns))

    def get_context(self, ctx_name):
        self._ctx = ctx_name
        return self.__assignment(self._ctx, self._name + ".getContext(\"2d\")")

    #region ATTRIBUTES 1
    def fill_style(self, color):
        return self.__assignment(self._ctx + ".fillStyle", color, True)

    def stroke_style(self, color):
        return self.__assignment(self._ctx + ".strokeStyle", color, True)

    def shadow_color(self, color):
        return self.__assignment(self._ctx + ".shadowColor", color, True)

    def shadow_blur(self, number):
        return self.__assignment(self._ctx + ".shadowBlur", number)

    def shadow_offset_x(self, offset_x):
        return self.__assignment(self._ctx + ".shadowOffsetX", offset_x)

    def shadow_offset_y(self, offset_y):
        return self.__assignment(self._ctx + ".shadowOffsetY", offset_y)
    #endregion

    def create_linear_gradient(self, x0, y0, x1, y1): #  Can be used as fillStyle !!
        grd_name = self.__get_grad_name()
        self._gradients.append(grd_name)
        return "var " + grd_name + " = " + self._ctx + \
               ".createLinearGradient( " + str(x0) + ", " + str(y0) + ", " + str(x1) + ", " + str(y1) + ");\r\n"

    def create_pattern(self, patternable_obj, pattern_type):
        pattern_name = self.__get_pattern_name()
        self._patterns.append(pattern_name)
        return "var " + pattern_name + " = " + self._ctx + ".createPattern(" + patternable_obj + ", \"" + pattern_type + "\");\r\n"

    # region LINE ATTRIBUTES
    def line_cap(self, line_style):
        return self.__assignment(self._ctx + ".lineCap", line_style, True)

    def line_join(self, join_type):
        return self.__assignment(self._ctx + ".lineJoin", join_type, True)

    def line_width(self, width):
        return self.__assignment(self._ctx + ".lineWidth", width)

    def miter_limit(self, miter_length):
        return self.__assignment(self._ctx + ".miterLimit", miter_length)
    # endregion

    # region RECTANGLE METHODS
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
    # endregion

    # region PATH STUFF
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
        return self._ctx + ".arc(" + str(x) + ", " + str(y) + ", " + str(r) + ", " + str(start_angle) + ", " + str(end_angle) + ", " + str(counterclockwise) + ");\r\n"

    def arc_to(self, x0, y0, x1, y1, r):
        return self._ctx + ".arcTo(" + str(x0) + ", " + str(y0) + "," + str(x1) + ", " + str(y1) + ", " + str(r) + ");\r\n"

    # ATTENTION --->>>> NO SEMICOLON NOR NEWLINE!
    def is_point_in_path(self, x, y):
        return self._ctx + ".isPointInPath(" + str(x) + ", " + str(y) + ")"
    # ------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------
    # endregion

    def scale(self, x, y):
        return self._ctx + ".scale(" + str(x) + ", " + str(y) + ");\r\n"

    def rotate(self, angle):
        return self._ctx + ".rotate(" + str(angle) + ");\r\n"

    def translate(self, x, y):
        return self._ctx + ".translate(" + str(x) + ", " + str(y) + ");\r\n"

    def transform(self, a ,b, c, d, e, f):
        return self._ctx + ".transform(" + str(a) + ", " + str(b) + ", " + str(c) + ", " + str(d) + ", " + str(e) + ", " + str(f) + ");\r\n"

    def set_transform(self, a, b, c, d, e, f):
        return self._ctx + ".setTransform(" + str(a) + ", " + str(b) + ", " + str(c) + ", " + str(d) + ", " + str(e) + ", " + str(f) + ");\r\n"

    # region TEXT ATTRIBUTES
    def font(self, size_and_font_name):
        return self.__assignment(self._name + ".font", size_and_font_name, True)

    def text_align(self, text_alignment):
        return self.__assignment(self._name + ".textAlign", text_alignment, True)

    def text_baseline(self, text_baseline):
        return self.__assignment(self._name + ".textBaseline", text_baseline, True)
    # endregion

    def fill_text(self, text, x, y):
        return self._ctx + ".fillText(\"" + text + "\", " + str(x) + ", " + str(y) + ");\r\n"

    def stroke_text(self, text, x, y):
        return self._ctx + ".strokeText(\"" + text + "\", " + str(x) + ", " + str(y) + ");\r\n"

    def measure_text(self, text, text_is_variable_name=False):
        var_name = "int_" + str(len(self._ints))
        self.__add_int_var(var_name)
        return "var " + var_name + " = " + self._ctx + ".measureText(\"" + text + "\").width;\r\n" \
               if not text_is_variable_name else \
               "var " + var_name + " = " + self._ctx + ".measureText(" + text + ").width\r\n"

    def draw_image(self, drawable_obj, x, y):
        return self._ctx + ".drawImage(" + drawable_obj + ", " + str(x) + ", " + str(y) + ");\r\n"

    @staticmethod
    def __assignment(left_of_eq, right_of_eq, quotes=False):
        return str(left_of_eq) + " = \"" + str(right_of_eq) + "\";\r\n" if quotes else str(left_of_eq) + " = " + str(right_of_eq) + ";\r\n"


class CanvasWebGl:
    def __init__(self):
        pass
