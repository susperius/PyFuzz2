__author__ = 'susperius'

import fuzzing.javascript as js

fuzzy = js.JsFuzz(10, 100, "ff")
for i in range(10):
    with open("test"+str(i)+".html", "w+") as fd:
        fd.write(fuzzy.fuzz(False))