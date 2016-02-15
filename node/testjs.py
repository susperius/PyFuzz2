__author__ = 'susperius'

from node.fuzzing.browser.javascript_ng import *

fuzzer = JsFuzzer(0, 10, 5, 5, 5, 'html')

print(fuzzer.fuzz())

