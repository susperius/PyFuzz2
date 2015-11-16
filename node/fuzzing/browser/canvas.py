import random
import jsfuzzer.JsCanvas as JsCanvas
from ..fuzzer import Fuzzer
from jsfuzzer.JsGlobal import JsGlobal
from jsfuzzer.values import FuzzValues

__author__ = 'susperius'


class CanvasFuzzer(Fuzzer):
    NAME = ['canvas_fuzzer']
    CONFIG_PARAMS = []

    def __init__(self, count, canvas_type="2d", canvas_id=""):
        self._count = count
        self._canvas_id = canvas_id
        self._canvas_type = canvas_type

    @classmethod
    def from_list(cls, params):
        raise NotImplementedError("ABSTRACT METHOD")

    @property
    def prng_state(self):
        return random.getstate()

    def set_canvas_id(self, canvas_id):
        self._canvas_id = canvas_id

    def fuzz(self):
        if self._canvas_type == "2d":
            js_canvas = JsCanvas.Canvas2d(self._canvas_id)
        else:
            return
        function = "function func_" + self._canvas_id + "() {\r\n"
        function += "var " + self._canvas_id + " = document.getElementById(\"" + self._canvas_id + "\");\r\n"
        function += js_canvas.get_context("ctx")
        for i in range(self._count):
            function += "\t"
            luck = random.choice(range(0, 10))
            if luck < 3:
                key = random.choice(js_canvas.attributes.keys())
                function += JsGlobal.try_catch_block(
                    js_canvas.attributes[key]["func"](random.choice(js_canvas.attributes[key]["parameter"])))
            else:
                method = random.choice(js_canvas.methods)
                if method == "create_linear_gradient":
                    x0, y0, x1, y1 = random.choice(js_canvas.ints), random.choice(js_canvas.ints), \
                                     random.choice(js_canvas.ints), random.choice(js_canvas.ints)
                    function += JsGlobal.try_catch_block(js_canvas.create_linear_gradient(x0, y0, x1, y1))
                elif method == "create_pattern":
                    function += JsGlobal.try_catch_block(
                        js_canvas.create_pattern(js_canvas.name, random.choice(js_canvas.PATTERN_TYPES)))
                elif method in js_canvas.rect_methods:
                    x, y, width, height = random.choice(js_canvas.ints), random.choice(js_canvas.ints), \
                                          random.choice(js_canvas.ints), random.choice(js_canvas.ints)
                    if method == "rect":
                        function += JsGlobal.try_catch_block(js_canvas.rect(x, y, width, height))
                    elif method == "fill_rect":
                        function += JsGlobal.try_catch_block(js_canvas.fill_rect(x, y, width, height))
                    elif method == "stroke_rect":
                        function += JsGlobal.try_catch_block(js_canvas.stroke_rect(x, y, width, height))
                    elif method == "clear_rect":
                        function += JsGlobal.try_catch_block(js_canvas.clear_rect(x, y, width, height))
                    elif method == "clip":
                        function += JsGlobal.try_catch_block(js_canvas.clip())
                elif method == "scale":
                    x, y = random.choice(js_canvas.ints), random.choice(js_canvas.ints)
                    function += JsGlobal.try_catch_block(js_canvas.scale(x, y))
                elif method == "rotate":
                    angle = random.choice(js_canvas.ints)
                    function += JsGlobal.try_catch_block(js_canvas.rotate(angle))
                elif method == "translate":
                    x, y = random.choice(js_canvas.ints), random.choice(js_canvas.ints)
                    function += JsGlobal.try_catch_block(js_canvas.translate(x, y))
                elif method == "transform" or method == "set_transform":
                    a, b, c, d, e, f = random.choice(js_canvas.ints), random.choice(js_canvas.ints), \
                                       random.choice(js_canvas.ints), random.choice(js_canvas.ints), \
                                       random.choice(js_canvas.ints), random.choice(js_canvas.ints)
                    function += JsGlobal.try_catch_block(js_canvas.transform(a, b, c, d, e, f)) \
                        if method == "transform" else \
                        JsGlobal.try_catch_block(js_canvas.set_transform(a, b, c, d, e, f))
                elif method == "fill_text" or method == "stroke_text":
                    x, y = random.choice(js_canvas.ints), random.choice(js_canvas.ints)
                    text = random.choice(FuzzValues.STRINGS)
                    function += JsGlobal.try_catch_block(js_canvas.fill_text(text, x, y)) \
                        if method == "fill_text" else \
                        JsGlobal.try_catch_block(js_canvas.stroke_text(text, x, y))
                elif method == "measure_text":
                    text = random.choice(FuzzValues.STRINGS)
                    function += JsGlobal.try_catch_block(js_canvas.measure_text(text))
                elif method == "draw_image":
                    x, y = random.choice(js_canvas.ints), random.choice(js_canvas.ints)
                    function += JsGlobal.try_catch_block(js_canvas.draw_image(js_canvas.name, x, y))
                elif method in js_canvas.path_methods:
                    if not js_canvas.has_active_path:
                        function += js_canvas.begin_path() + "\t"
                    if method == "stroke":
                        function += JsGlobal.try_catch_block(js_canvas.stroke())
                    elif method == "fill":
                        function += JsGlobal.try_catch_block(js_canvas.fill())
                    elif method == "move_to":
                        x, y = random.choice(js_canvas.ints), random.choice(js_canvas.ints)
                        function += JsGlobal.try_catch_block(js_canvas.move_to(x, y))
                    elif method == "close_path":
                        function += JsGlobal.try_catch_block(js_canvas.close_path())
                    elif method == "line_to":
                        x, y = random.choice(js_canvas.ints), random.choice(js_canvas.ints)
                        function += JsGlobal.try_catch_block(js_canvas.line_to(x, y))
                    elif method == "quadratic_curve_to":
                        cpx, cpy, x, y = random.choice(js_canvas.ints), random.choice(js_canvas.ints), \
                                         random.choice(js_canvas.ints), random.choice(js_canvas.ints)
                        function += JsGlobal.try_catch_block(js_canvas.quadratic_curve_to(cpx, cpy, x, y))
                    elif method == "bezier_curve_to":
                        cp1x, cp1y, cp2x, cp2y, x, y = random.choice(js_canvas.ints), random.choice(js_canvas.ints), \
                                                       random.choice(js_canvas.ints), random.choice(js_canvas.ints), \
                                                       random.choice(js_canvas.ints), random.choice(js_canvas.ints)
                        function += JsGlobal.try_catch_block(js_canvas.bezier_curve_to(cp1x, cp1y, cp2x, cp2y, x, y))
                    elif method == "arc":
                        x, y, r, start, end = random.choice(js_canvas.ints), random.choice(js_canvas.ints), \
                                              random.choice(js_canvas.ints), random.choice(js_canvas.ints), \
                                              random.choice(js_canvas.ints)
                        counter = random.choice(FuzzValues.BOOL)
                        function += JsGlobal.try_catch_block(js_canvas.arc(x, y, r, start, end, counter))
                    elif method == "arc_to":
                        x0, y0, x1, y1, r = random.choice(js_canvas.ints), random.choice(js_canvas.ints), \
                                            random.choice(js_canvas.ints), random.choice(js_canvas.ints), \
                                            random.choice(js_canvas.ints)
                        function += JsGlobal.try_catch_block(js_canvas.arc_to(x0, y0, x1, y1, r))
        if js_canvas.has_active_path:
            function += JsGlobal.try_catch_block(js_canvas.stroke())
        function += "}\r\n"
        return function


def set_state(self, state):
    raise NotImplementedError("ABSTRACT METHOD")


def set_seed(self, seed):
    raise NotImplementedError("ABSTRACT METHOD")


def create_testcases(self, count, directory):
    raise NotImplementedError("ABSTRACT METHOD")


@property
def file_type(self):
    raise NotImplementedError("ABSTRACT METHOD")
