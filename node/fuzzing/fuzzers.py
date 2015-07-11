__author__ = 'susperius'

import javascript
import bytemutation

FUZZERS = {bytemutation.ByteMutation.NAME: bytemutation.ByteMutation.CONFIG_PARAMS,
           javascript.JsDomFuzzer.NAME: javascript.JsDomFuzzer.CONFIG_PARAMS}