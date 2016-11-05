import random
from fuzzing.browser.browser_fuzzer import BrowserFuzzer


random.seed(0)

fuzzer = BrowserFuzzer(5, 2, 100, 10, '2d', 1, 30, 'html')


with open("test.html", 'w+') as fd:
    fd.write(fuzzer.fuzz()[0])


