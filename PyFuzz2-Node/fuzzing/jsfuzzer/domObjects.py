__author__ = "susperius"


class DomObjects:
    DOM_DOCUMENT_METHODS = ['addEventListener', 'adoptNode', 'close', 'createAttribute', 'createComment',
                            'createDocumentFragment', 'createElement', 'createTextNode', 'getElementById',
                            'getElementsByClassName', 'getElementsByName', 'getElementsByTagName', 'importNode',
                            'normalize', 'normalizeDocument', 'open', 'querySelector', 'querySelectorAll',
                            'removeEventListener', 'renameNode', 'write', 'writeln']
    DOM_DOCUMENT_PROPERTIES_READ_ONLY = ['anchors', 'applets', 'baseURI', 'cookie', 'doctype', 'documentElement',
                                         'documentMode', 'domain', 'domConfig', 'embeds', 'forms', 'head',
                                         'images', 'implementation', 'inputEncoding', 'lastModified', 'links',
                                         'readyState', 'referrer', 'scripts', 'URL']
    DOM_DOCUMENT_PROPERTIES_MODIFIABLE = ['body', 'documentURI', 'strictErrorChecking', 'title']
    DOM_DOCUMENT_AVOID_METHODS = ['hasAttributes']
    DOM_DOCUMENT_AVOID_PROPERTIES = ['attributes', 'nextSibling', 'nodeName', 'nodeType', 'nodeValue',
                                     'ownerDocument', 'ownerElement', 'parentNode', 'previousSibling', 'textContent']
    # END DOM DOCUMENT OBJECT
    # START DOM ELEMENT OBJECT
    DOM_ELEMENT_METHODS = ['addEventListener', 'appendChild', 'cloneNode',
                           'hasAttribute', 'insertBefore', 'normalize',
                           'removeAttribute', 'removeChild', 'replaceChild',
                           'removeEventListener', 'setAttribute', 'REPLACE_EXIST_ELEMENT']
    #'hasChildNodes' , 'MIX_REFERENCES'
    DOM_ELEMENT_EVENT_METHODS = ['blur', 'click', 'focus', ]
    DOM_ELEMENT_AVOID_METHODS = ['getAttributeNode', 'hasAttributes', 'setAttributeNode', 'isSupported',
                                 'querySelector', 'querySelectorAll', 'getElementsByClassName',
                                 'getElementsByTagName', 'getAttribute', 'getFeature', 'getUserData',
                                 'removeAttributeNode', 'toString''isDefaultNameSpace', 'isEqualNode', 'isSameNode', ]
    DOM_ELEMENT_PROPERTIES_READ_ONLY = ['attributes', 'childNodes', 'clientHeight', 'clientWidth', 'firstChild',
                                        'lastChild',
                                        'namespaceURI', 'nextSibling', 'nodeName', 'nodeType', 'offsetHeight',
                                        'offsetWidth',
                                        'offsetLeft', 'offsetRight', 'offsetParent', 'offsetTop', 'ownerDocument',
                                        'parentNode',
                                        'previousSibling', 'scrollHeight', 'scrollWidth', 'tagName', 'length',
                                        'isContentEditable']
    DOM_ELEMENT_PROPERTIES_MODIFIABLE = ['className', 'contentEditable', 'dir', 'id',
                                         'innerHTML', 'lang',
                                         'scrollLeft', 'scrollTop', 'style', 'tabIndex', 'textContent', 'title']
    DOM_ELEMENT_AVOID_PROPERTIES_MODIFIABLE = ['compareDocumentPosition', 'nodeValue', ]

    DOM_ELEMENT_FUZZ_STUFF = DOM_ELEMENT_METHODS + DOM_ELEMENT_PROPERTIES_MODIFIABLE
    # END DOM ELEMENT OBJECT

    # START DOM ATTRIBUTE NODEMAP OBJECT
    DOM_NODEMAP_METHODS = ['getNamedItem', 'item', 'removeNamedItem', 'setNamedItem']
    DOM_ATTR_PROPERTIES_READ_ONLY = ['isId', 'name', 'specified']
    DOM_ATTR_PROPERTIES_MODIFIABLE = ['value']
    # END DOM ATTRIBUTE NODEMAP OBJECT

    # START DOM EVENTS
    DOM_EVENTS_MOUSE = ['onclick', 'oncontextmenu', 'ondblclick', 'onmousedown', 'onmouseenter', 'onmouseleave',
                        'onmouseover', 'onmouseout',
                        'onmouseup']
    DOM_EVENTS_KEYBOARD = ['onkeydown', 'onkeypress', 'onkeyup']
    DOM_EVENTS_FRAME = ['onabort', 'onbeforeunload', 'onerror', 'onhashchange', 'onload', 'onpageshow', 'onpagehide',
                        'onresize', 'onscroll', 'onunload']
    DOM_EVENTS_FORM = ['onblur', 'onchange', 'onfocus', 'onfocusin', 'oninput', 'oninvalid', 'onreset', 'onsearch',
                       'onselect', 'onsubmit']
    DOM_EVENTS_DRAG = ['ondrag', 'ondragend', 'ondragenter', 'ondragleave', 'ondragover', 'ondragstart', 'ondrop']
    DOM_EVENTS_CLIPBOARD = ['oncopy', 'oncut', 'onpaste']
    DOM_EVENTS_PRINT = ['onafterprint', 'onbeforeprint']
    DOM_EVENTS_MEDIA = ['onabort', 'oncanplay', 'oncanplaythrough', 'ondurationchange', 'onemptied', 'onended',
                        'onerror', 'onloaddata', 'onloadedmetadata',
                        'onloadstart', 'onpause', 'onplay', 'onplaying', 'onprogress', 'onratechange', 'onseeked',
                        'onseeking', 'onstalled', 'onsuspend',
                        'ontimeupdate', 'onvolumechange', 'onwaiting']
    DOM_EVENTS_ANIMATION = ['animationend', 'animationiteration', 'animationstart']
    DOM_EVENTS_TRANSITION = ['transitionend']
    DOM_EVENTS_MISC = ['onmessage', 'onmousewheel', 'ononline', 'onoffline', 'onpopstate', 'onshow', 'onstoreage',
                       'ontoggle', 'onwheel']
    DOM_EVENTS_USABLE = ['click', 'error', 'load', 'scroll', 'resize', 'change', 'focus', 'focusin', 'blur', 'select',
                         'pageshow', 'unload', 'beforeunload']

    DOM_MUTATION_EVENTS = ['DOMAttrModified', 'DOMAttributeNameChanged', 'DOMCharacterDataModified',
                           'DOMElementNameChanged', 'DOMNodeInserted', 'DOMNodeRemoved', 'DOMNodeRemoved',
                           'DOMNodeRemovedFromDocument', 'DOMSubtreeModified']

    DOM_EVENTS = DOM_EVENTS_USABLE + DOM_MUTATION_EVENTS
    # END DOM EVENTS

    # START DOM EVENT OBJECT
    DOM_EVENT_CONSTANTS = ['CAPTURING_PHASE', 'AT_TARGET', 'BUBBLING_PHASE']
    DOM_EVENT_PROPERTIES_READ_ONLY = ['bubbles', 'cancelable', 'currentTarget', 'defaultPrevented', 'eventPhase',
                                      'isTrusted', 'target', 'timeStamp',
                                      'type', 'view']
    # END DOM EVENT OBJECT

    # START DOM EVENTARGET OBJECT
    DOM_EVENTTARGET_METHODS = ['addEventListener', 'dispatchEvent', 'removeEventListener']
    # END DOM EVENTTARGET OBJECT

    # START EVENTLISTENER OBJECT
    DOM_EVENTLISTENER_OBJECT_METHODS = ['handleEvent']
    # END EVENTLISTENER OBJECT

    # START DOCUMENTEVENT OBJECT
    DOM_DOCUMENTEVENT_OBJECT_METHODS = ['createEvent']
    # END DOCUMENTEVENT OBJECT

    # START MOUSEEVENT OBJECT
    DOM_MOUSEEVENT_OBJECT_METHODS = ['initMouseEvent']
    DOM_MOUSEEVENT_OBJECT_PROPERTIES_READ_ONLY = ['altKey', 'button', 'buttons', 'clientX', 'clientY', 'ctrlKey',
                                                  'detail', 'metaKey', 'relatedTarget',
                                                  'screenX', 'screenY', 'shiftKey', 'which']
    # END MOUSEEVENT OBJECT

    # START KEYBOARDEVENT OBJECT
    DOM_KEYBOARDEVENT_OBJECT_METHODS = ['initKeyboardEvent']
    DOM_KEYBOARDEVENT_OBJECT_PROPERTIES_READ_ONLY = ['altKey', 'ctrlKey', 'charCode', 'key', 'keyCode', 'location',
                                                     'metaKey', 'shiftKey', 'which']
