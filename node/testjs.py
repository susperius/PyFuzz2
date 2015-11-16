__author__ = 'susperius'

import node.fuzzing.browser.javascript as fuzz_js
import node.fuzzing.browser.canvas as fuzz_canv

# fuzzy = fuzz_js.JsDomFuzzer(600, 5000, "ie")

'''
for i in range(10):
    with open('test'+str(i)+'.html', 'w+') as fd:
        fd.write(fuzzy.fuzz())

'''
'''
case = fuzzy.fuzz()
reducer = red_js.JsReducer(case, 'abc')

for i in range(30):
    print(i)
    with open('red_case'+str(i)+'.html', 'w+') as fd:
        red = reducer.reduce()
        if red is not None:
            fd.write(reducer.reduce())
        else:
            quit()
    reducer.crashed(True)
'''

fuzzy = fuzz_canv.CanvasFuzzer(200)
fuzzy.set_canvas_id("canvas01")
print(fuzzy.fuzz())
