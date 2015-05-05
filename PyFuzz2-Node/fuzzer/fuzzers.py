__author__ = 'susperius'

import javascript
import bytemutation

FUZZERS = {bytemutation.ByteMutation.NAME: bytemutation.ByteMutation.CONFIG_PARAMS,
           javascript.JsFuzz.NAME: javascript.JsFuzz.CONFIG_PARAMS}