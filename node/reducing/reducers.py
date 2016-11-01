__author__ = 'susperius'

import javascript
import css

REDUCERS = {javascript.JsReducer.NAME: (javascript.JsReducer.CONFIG_PARAMS, javascript.JsReducer),
            css.CSSReducer.NAME: (css.CSSReducer.CONFIG_PARAMS, css.CSSReducer)}

def get_reducer(reducer_type, config):
    return REDUCERS[reducer_type].from_list(config)