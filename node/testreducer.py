import reducing.javascript
import logging

formatter = logging.Formatter("%(levelname)s: %(message)s")
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

red = reducing.javascript.JsReducer("html")

red.set_case("./", "test56.html")


case = red.reduce()
red.crashed(False)

case = red.reduce()
red.crashed(True)
print(len(case))

case = red.reduce()
red.crashed(True)
print(len(case))

case = red.reduce()
red.crashed(True)
print(len(case))
"""
case = red.reduce()
red.crashed(True)
print(len(case))

case = red.reduce()
red.crashed(True)
print(len(case))

case = red.reduce()
red.crashed(True)
print(len(case))

case = red.reduce()
red.crashed(True)
print(len(case))

case = red.reduce()
red.crashed(True)
print(len(case))

case = red.reduce()
red.crashed(True)
print(len(case))

while case is not None:
    case = red.reduce()
    red.crashed(True)
    print(len(case))

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
    #red.crashed(True)

