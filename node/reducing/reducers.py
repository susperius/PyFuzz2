__author__ = 'susperius'

import javascript
import css
import browser_reducer

REDUCERS = {javascript.JsReducer.NAME: (javascript.JsReducer.CONFIG_PARAMS, javascript.JsReducer),
            css.CSSReducer.NAME: (css.CSSReducer.CONFIG_PARAMS, css.CSSReducer),
            browser_reducer.BrowserTestcaseReducer.NAME: (browser_reducer.BrowserTestcaseReducer.CONFIG_PARAMS,
                                                          browser_reducer.BrowserTestcaseReducer)}


def get_reducer(reducer_type, config):
    return REDUCERS[reducer_type][1].from_list(config)