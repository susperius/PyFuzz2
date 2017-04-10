import random
from fuzzing.browser.browser_fuzzer import BrowserFuzzer
from fuzzing.regex_fuzzer import RegExFuzzer

random.seed(0)


fuzzer = BrowserFuzzer(30, 2, 100, 10, 30, 'html')

fuzzer.create_testcases(10, './testcases/')




"""
fuzzer = RegExFuzzer(45)

for i in range(20000):
    print(fuzzer.fuzz())
"""
