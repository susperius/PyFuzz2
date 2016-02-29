__author__ = 'susperius'

from node.fuzzing.browser.javascript_ng import *

fuzzer = JsFuzzer(15, 10, 5, 5, 5, 500, 20, 'html')

#fuzzer.create_testcases(2, ".")

print(fuzzer.test())
