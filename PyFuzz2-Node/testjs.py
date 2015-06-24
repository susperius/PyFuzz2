__author__ = 'susperius'

import fuzzing.javascript as js

fuzzy = js.JsDomFuzzer(10, 100, "ie")
print(fuzzy.fuzz())