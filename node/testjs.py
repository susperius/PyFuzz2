__author__ = 'susperius'

import fuzzing.javascript as js

fuzzy = js.JsDomFuzzer(100, 2000, "ie")

for i in range(10):
    with open('test'+str(i)+'.html', 'w+') as fd:
        fd.write(fuzzy.fuzz())
