import reducing.javascript


red = reducing.javascript.JsReducer("html")

red.set_case("./", "test56.html")



case = red.reduce()
red.crashed(True)
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
"""

with open("red00.html", 'wb+') as fd:
    case = red.reduce()
    print(case)
    fd.write(case)
    red.crashed(True)

