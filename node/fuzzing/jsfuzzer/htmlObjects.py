__author__ = "susperius"


class HtmlObjects:
    HTML_OBJECTS = ['a', 'abbr', 'address', 'area', 'article', 'aside', 'audio', 'b', 'base', 'bdo', 'blockquote',
                    'body',
                    'br', 'button', 'canvas', 'caption', 'cite', 'code', 'col', 'colgroup', 'datalist', 'dd', 'del',
                    'details',
                    'dfn', 'dialog', 'div', 'dl', 'dt', 'em', 'embed', 'fieldset', 'figcaption', 'figure', 'footer',
                    'form',
                    'head', 'header', 'hgroup', 'h1', 'h6', 'hr', 'html', 'i', 'iframe', 'img', 'ins', 'input,' 'kbd',
                    'keygen',
                    'label', 'legend', 'li', 'link', 'map', 'mark', 'menu', 'menuitem', 'meta', 'meter', 'nav',
                    'object',
                    'ol', 'optgroup', 'option', 'output', 'p', 'param', 'pre', 'progress', 'q', 's', 'samp', 'script',
                    'section', 'select', 'small', 'source', 'span', 'strong', 'style', 'sub', 'summary', 'sup', 'table',
                    'td',
                    'th', 'tr', 'textarea', 'time', 'title', 'track', 'u', 'ul', 'var', 'video']

    HTML_INPUT_TYPES = ['password', 'button', 'checkbox', 'color', 'date', 'datetime', 'datetime-local', 'email',
                        'file', 'hidden', 'image', 'month', 'number', 'radio', 'range', 'reset', 'search', 'submit',
                        'text', 'time', 'url', 'week']

    HTML_ATTR_GENERIC = ['class', 'id', 'style', 'title']

#  #  #  #  #  #  #  #  #  #  #  #  #  #  # HTML5 #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

    #  Types: APP_DATA, BOOL, BUTTON_TYPE, CHAR, CHARACTER_SET, COORDS, CSS, CSS_CLASS, DATETIME, DIRECTION, ELEM_ID, FORM_ID, FORM_METHOD, FORM_TARGET,
    #         FORM_ENCTYPE, HEADERS_ID, HTML_CODE, HTTP_EQUIV, INT, ID, LANG, MAP_NAME, MEDIA_TYPE, MEDIA_QUERY, MENU, METADATA_NAME, ONOFF, PIXELS, PRELOAD, REL, SCROLLING, SHAPE,
    #         SANDBOX, SORTED, STRING, TABLE_SCOPE, TARGET, TRACK_KIND, URL, WRAP
    #
    HTML5_GLOBAL_ATTR = {'accesskey': 'CHAR', 'class': 'CSS_CLASS', 'contenteditable': 'BOOL', 'contextmenu': 'MENU',
                         'data-': 'APP_DATA', 'dir': 'DIRECTION', 'dragable': 'BOOL', 'hidden': 'BOOL', 'id': 'ID',
                         'lang': 'LANG', 'spellcheck': 'BOOL', 'style': 'CSS', 'tabindex': 'INT', 'title': 'STRING',
                         'translate': 'BOOL'}

    HTML5_A_ATTR = {'download': 'STRING', 'href': 'URL', 'hreflang': 'LANG', 'media': 'MEDIA_QUERY', 'rel': 'REL',
                    'target': 'TARGET', 'type': 'MEDIA_TYPE'}

    HTML5_AREA_ATTR = dict({'alt': 'STRING', 'coords': 'COORDS', 'shape': 'SHAPE'}.items() + HTML5_A_ATTR.items())

    HTML5_AUDIO_ATTR = {'autoplay': 'BOOL', 'controls': None, 'loop': None, 'muted': None, 'preload': 'PRELOAD',
                        'src': 'URL'}

    HTML5_BASE_ATTR = {'href': 'URL', 'target': 'TARGET'}

    HTML5_BLOCKQOUTE_ATTR = {'cite': 'URL'}

    HTML5_BUTTON_ATTR = {'autofocus': None, 'disabled': None, 'formEnctype': 'FORM_ENCTYPE',
                         'formMethod': 'FORM_METHOD', 'formNoValidate': 'BOOL', 'formTarget': 'FORM_TARGET',
                         'name': 'STRING', 'type': 'BUTTON_TYPE', 'value': 'STRING'}

    HTML5_COL_ATTR = {'span': 'INT'}

    HTML5_DEL_ATTR = {'cite': 'URL', 'datetime': 'DATETIME'}

    HTML5_DETAILS_ATTR = {'open': None}

    HTML5_EMBED_ATTR = {'height': 'PIXELS', 'src': 'URL', 'type': 'MEDIA_TYPE', 'width': 'PIXELS'}

    HTML5_FIELDSET_ATTR = {'disabled': None, 'form': 'FORM_ID', 'name': 'STRING'}

    HTML5_FORM_ATTR = {'accept-charset': 'CHARACTER_SET', 'action': 'URL', 'autocomplete': 'ONOFF',
                       'enctype': 'FORM_ENCTYPE', 'method': 'FORM_METHOD', 'name': 'STRING', 'novalidate': None,
                       'target': 'TARGET'}

    HTML5_IFRAME_ATTR = {'name': 'STRING', 'sandbox': 'SANDBOX', 'scrolling': 'SCROLLING', 'seamless': None,
                         #'src': 'URL',
                         'srcdoc': 'HTML_CODE', 'width': 'PIXELS'}

    HTML5_IMG_ATTR = {'alt': 'STRING', 'crossorigin': 'CROSSORIGIN', 'height': 'PIXELS', 'ismap': None,
                      'longdesc': 'URL', 'src': 'URL', 'usemap': 'MAP_NAME', 'width': 'PIXELS'}

    HTML5_INPUT_ATTR = {'accept': 'MEDIA_TYPE', 'alt': 'STRING', 'autocomplete': 'ONOFF', 'autofocus': None,
                        'checked': None, 'disabled': None, 'form': 'FORM_ID', 'formaction': 'URL',
                        'formenctype': 'FORM_ENCTYPE', 'formmethod': 'FORM_METHOD', 'formnovalidate': None,
                        'formtarget': 'FORM_TARGET', 'height': 'PIXELS', 'list': 'DATALIST_ID', 'max': 'INT',
                        'maxlength': 'INT', 'min': 'INT', 'multiple': None, 'name': 'STRING', 'pattern': 'REGEXP',
                        'placeholder': 'STRING', 'readonly': None, 'required': None, 'size': 'INT',
                        #'src': 'URL',
                        'step': 'INT', 'type': 'INPUT_TYPE', 'value': 'STRING', 'width': 'PIXELS' }

    HTML5_KEYGEN_ATTR = {'autofocus': None, 'challenge': None, 'disabled': None, 'form': 'FORM_ID',
                         'keytype': 'KEYTYPE', 'name': 'STRING'}

    HTML5_LABEL_ATTR = {'for': 'ELEM_ID', 'form': 'FORM_ID'}

    HTML5_LI_ATTR = {'value': 'INT'}

    HTML5_MAP_ATTR = {'name': 'STRING'}

    HTML5_META_ATTR = {'charset': 'CHARACTER_SET', 'content': 'STRING', 'http-equiv': 'HTTP_EQUIV',
                       'name': 'METADATA_NAME'}

    HTML5_METER_ATTR = {'form': 'FORM_ID', 'high': 'INT', 'low': 'INT', 'max': 'INT', 'min': 'INT', 'optimum': 'INT',
                        'value': 'INT'}

    HTML5_OBJECT_ATTR = {'data': 'URL', 'form': 'FORM_ID', 'height': 'PIXELS', 'type': 'MEDIA_TYPE',
                         'usemap': 'MAP_NAME', 'width': 'PIXELS'}

    HTML5_OPTGROUP_ATTR = {'disabled': None, 'label': 'STRING'}

    HTML5_OPTION_ATTR = {'disabled': None, 'label': 'STRING', 'selected': None, 'value': 'STRING'}

    HTML5_OUTPUT_ATTR = {'for': 'ELEM_ID', 'form': 'FORM_ID', 'name': 'STRING'}

    HTML5_PROGRESS_ATTR = {'max': 'INT', 'value': 'INT'}

    HTML5_Q_ATTR = {'cite': 'URL'}

    HTML5_SCRIPT_ATTR = {'async': None, 'charset': 'CHARACTER_SET', 'defer': None, 'src': 'URL', 'type': 'MEDIA_TYPE'}

    HTML5_SELECT_ATTR = {'autofocus': None, 'disabled': None, 'form': 'FORM_ID', 'multiple': None, 'name': 'STRING',
                         'required': None, 'size': 'INT'}

    HTML5_SOURCE_ATTR = {'media': 'MEDIA_QUERY', 'src': 'URL', 'type': 'MEDIA_TYPE'}

    HTML5_STYLE_ATTR = {'media': 'MEDIA_QUERY', 'scoped': None, 'type': 'MEDIA_TYPE'}

    HTML5_TABLE_ATTR = {'sortable': None}

    HTML5_TD_ATTR = {'colspan': 'INT', 'headers': 'HEADER_ID', 'rowspan': 'INT'}

    HTML5_TEXTAREA_ATTR = {'autofocus': None, 'cols': 'INT', 'disabled': None, 'form': 'FORM_ID', 'maxlength': 'INT',
                      'name': 'STRING', 'placeholder': 'STRING', 'readonly': None, 'required': None, 'rows': 'INT',
                           'wrap': 'WRAP'}

    HTML5_TH_ATTR = {'abbr': 'STRING', 'colspan': 'INT', 'headers': 'HEADER_ID', 'rowspan': 'INT', 'scope': 'TABLE_SCOPE',
                     'sorted': 'SORTED'}

    HTML5_TIME_ATTR = {'datetime': 'DATETIME'}

    HTML5_TRACK_ATTR = {'default': None, 'kind': 'TRACK_KIND', 'label': 'STRING', 'src': 'URL', 'srclang': 'LANG'}

    HTML5_VIDEO_ATTR = {'autoplay': None, 'controls': None, 'height': 'PIXELS', 'loop': None, 'muted': None, 'poster': 'URL',
                        'preload': 'PRELOAD', 'src': 'URL', 'width': 'PIXELS'}

    #  Dict Layout = { 'tag_name': {'outer_tag': ['tag_name', ...] | None, 'attr': {'attr_name': TYPE, ...}, 'req_tag': ['tag_name', ...] | None}
    HTML5_OBJECTS = {'a': {'outer_tag': None, 'attr': dict(HTML5_A_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': ['href']},
                     'abbr': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': ['title']},
                     'address': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'area': {'outer_tag': ['map'], 'attr': dict(HTML5_AREA_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': None},
                     'article': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'aside': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'audio': {'outer_tag': None, 'attr': dict(HTML5_AUDIO_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': None},
                     'b': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'base': {'outer_tag': ['head'], 'attr': dict(HTML5_BASE_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': ['href']},
                     #'bdi': ,
                     'bdo': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': ['dir']},
                     'blockquote': {'outer_tag': None, 'attr': dict(HTML5_BLOCKQOUTE_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': ['cite']},
                     'body': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'br': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'button': {'outer_tag': None, 'attr': dict(HTML5_BUTTON_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': None},
                     #'canvas': ,
                     'caption': {'outer_tag': ['table'], 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     #'center': ,
                     'cite': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'code': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'col': {'outer_tag': ['colgroup'], 'attr': dict(HTML5_COL_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': ['span']},
                     'colgroup': {'outer_tag': ['table'], 'attr': dict(HTML5_COL_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': None},
                     'datalist': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'dd': {'outer_tag': ['dl'], 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'del': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': ['cite']},
                     'details': {'outer_tag': None, 'attr': dict(HTML5_DETAILS_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': ['open']},
                     'dfn': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'dialog': {'outer_tag': None, 'attr': dict(HTML5_DETAILS_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': ['open']},
                     #'dir':,
                     'div': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': ['style']},
                     'dl': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'dt': {'outer_tag': ['dl'], 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'em': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'embed': {'outer_tag': None, 'attr': dict(HTML5_EMBED_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': None},
                     'fieldset': {'outer_tag': ['form'], 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'figcaption': {'outer_tag': ['figure'], 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'figure': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     #'font':,
                     'footer': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'form': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     #'frame':,
                     #'frameset':,
                     'h1': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'h2': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'h3': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'h4': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'h5': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'h6': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'head': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'header': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'hr': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'html': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'i': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'iframe': {'outer_tag': None, 'attr': dict(HTML5_IFRAME_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': ['srcdoc']},
                     'img': {'outer_tag': None, 'attr': dict(HTML5_IMG_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': None},
                     'input': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'ins': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'kbd': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'keygen': {'outer_tag': ['form'], 'attr': dict(HTML5_KEYGEN_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': None},
                     'label': {'outer_tag': ['form'], 'attr': dict(HTML5_LABEL_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': None},
                     'legend': {'outer_tag': ['fieldset'], 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'li': {'outer_tag': ['ol' 'ul'], 'attr': dict(HTML5_LI_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': None},
                     #'link': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'main': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'map': {'outer_tag': None, 'attr': dict(HTML5_MAP_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': None},
                     'mark': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     #'menu':,
                     #'menuitem':,
                     'meta': {'outer_tag': ['head'], 'attr': dict(HTML5_META_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': ['content', 'name']},
                     'meter': {'outer_tag': None, 'attr': dict(HTML5_METER_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': ['value']},
                     'nav': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     #'noframes':,
                     #'noscript':,
                     'object': {'outer_tag': None, 'attr': dict(HTML5_OBJECT_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': None},
                     'ol': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'optgroup': {'outer_tag': ['select'], 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'option': {'outer_tag': ['select', 'optgroup'], 'attr': dict(HTML5_OPTION_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': None },
                     'output': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'p': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     #'param': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'pre': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'progress': {'outer_tag': None, 'attr': dict(HTML5_PROGRESS_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': ['max', 'value']},
                     'q': {'outer_tag': None, 'attr': dict(HTML5_Q_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': None},
                     'rp': {'outer_tag': ['ruby'], 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'rt': {'outer_tag': ['ruby'], 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'ruby': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     's': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'samp': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'script': {'outer_tag': None, 'attr': dict(HTML5_SCRIPT_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': None},
                     'section': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'select': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'small': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'source': {'outer_tag': ['audio', 'video'], 'attr': dict(HTML5_SOURCE_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': None},
                     'span': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     #'strike': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'strong': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'style': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'sub': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'summary': {'outer_tag': ['details'], 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'sup': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'table': {'outer_tag': None, 'attr': dict(HTML5_TABLE_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': None},
                     'tbody': {'outer_tag': ['table'], 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'td': {'outer_tag': ['tr'], 'attr': dict(HTML5_TD_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': None},
                     'textarea': {'outer_tag': None, 'attr': dict(HTML5_TEXTAREA_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': None},
                     'tfoot': {'outer_tag': ['table'], 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'th': {'outer_tag': ['tr'], 'attr': dict(HTML5_TH_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': None},
                     'thead': {'outer_tag': ['table'], 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'time': {'outer_tag': None, 'attr': dict(HTML5_TIME_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': None},
                     'title': {'outer_tag': ['head'], 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'tr': {'outer_tag': ['table'], 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'track': {'outer_tag': None, 'attr': dict(HTML5_TRACK_ATTR.items() + HTML5_GLOBAL_ATTR.items()), 'req_tag': None},
                     #'tt':,
                     'u': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'ul': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'var': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'video': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None},
                     'wbr': {'outer_tag': None, 'attr': HTML5_GLOBAL_ATTR, 'req_tag': None}
                    }