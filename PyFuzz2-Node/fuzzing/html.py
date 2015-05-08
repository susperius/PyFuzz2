__author__ = 'susperius'

import jsfuzzer.htmlObjects as htmlObjects
import random
from jsfuzzer.htmlObjects import HtmlObjects

TEMPLATE_FILE = "fuzzing/jsfuzzer/template.dat"


class HtmlFuzzer:

    def __init__(self, count, depth=1, seed=31337):
        self._text = ["AAAAAAAAAA", "BBBBBBBBBB", "CCCCCCCCCC", "DDDDDDDDDD", "EEEEEEEEEE"]
        self._count = count
        self._depth = depth
        random.seed(seed)

    def fuzz(self):
        id_comment = "<!-- IDS: "
        objects = ""
        for i in range(self._count):
            obj = self._get_no_script_tag()
            open_tag, inner, close_tag = self._create_html_object(obj, "id"+str(i))
            id_comment += "id" + str(i) + "; "
            open_tag += "\n"
            inner += "\n"
            for j in range(random.randint(0, self._depth)):
                obj = self._get_no_script_tag()
                in_open_tag, in_inner, in_close_tag = self._create_html_object(obj,
                                                                               "id" + str(i) + str(j))
                id_comment += "id" + str(i) + str(j) + "; "
                inner += in_open_tag + in_inner + in_close_tag
            objects += open_tag + inner + close_tag
        id_comment += "-->"
        objects += id_comment
        with open(TEMPLATE_FILE, "r") as fd:
            template = fd.read()
        return template.replace("HTML_BODY", objects)

    def _get_no_script_tag(self):
        obj = "script"
        while obj == "script":
            obj = random.choice(HtmlObjects.HTML_OBJECTS)
        return obj

    def _create_html_object(self, tag, ident):
        text = random.choice(self._text)
        open_tag = "<" + tag + " id=\"" + ident + "\"> "
        close_tag = " </" + tag + ">\n"
        return open_tag, text, close_tag