__author__ = 'susperius'

import javascript
import css

REDUCERS = {javascript.JsReducer.NAME: (javascript.JsReducer.CONFIG_PARAMS, javascript.JsReducer),
            css.CSSReducer.NAME: (css.CSSReducer.CONFIG_PARAMS, css.CSSReducer)}
