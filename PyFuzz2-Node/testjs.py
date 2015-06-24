__author__ = 'susperius'

import fuzzing.js_dom as js

fuzzy = js.JsDomFuzzer(10, 100, "ie")
print(fuzzy.fuzz())