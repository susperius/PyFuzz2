import reducing.javascript


red = reducing.javascript.JsReducer("html")

red.set_case("./", "reduced2.html")

# case = red.test()


case = red.reduce()
red.crashed(False)


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
"""

with open("red00.html", 'wb+') as fd:
    fd.write(case)
    red.crashed(True)

