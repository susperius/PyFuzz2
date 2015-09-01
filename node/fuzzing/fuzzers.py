__author__ = 'susperius'

import browser.javascript as javascript
import bytemutation

"""
If you want to implement a new fuzzer just inherit from the Fuzzer Class and implement the abstract methods.
After this add a column for your fuzzer.
The dictionary key is the fuzzers name and the contents is a tupel with all the necessary configuration
parameters as first value and a reference to your fuzzers class as the second value.
"""

FUZZERS = {bytemutation.ByteMutation.NAME: (bytemutation.ByteMutation.CONFIG_PARAMS, bytemutation.ByteMutation),
           javascript.JsDomFuzzer.NAME: (javascript.JsDomFuzzer.CONFIG_PARAMS, javascript.JsDomFuzzer)}