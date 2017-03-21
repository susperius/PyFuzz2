import random
from fuzzing.browser.browser_fuzzer import BrowserFuzzer


random.seed(0)

fuzzer = BrowserFuzzer(5, 2, 100, 10, 30, 'html')

fuzzer.create_testcases(10, './testcases/')


