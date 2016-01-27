import reducing.javascript


red = reducing.javascript.JsReducer("html")

red.set_case("./", "test00.html")

"""
case = red.reduce()
red.crashed(True)
case = red.reduce()
red.crashed(True)
case = red.reduce()
red.crashed(True)
case = red.reduce()
red.crashed(True)
case = red.reduce()
red.crashed(True)
case = red.reduce()
red.crashed(True)
case = red.reduce()
red.crashed(True)
case = red.reduce()
red.crashed(True)
case = red.reduce()
red.crashed(True)
case = red.reduce()
red.crashed(True)
"""

with open("red00.html", 'wb+') as fd:
    case = red.reduce()
    fd.write(case)
    red.crashed(True)

