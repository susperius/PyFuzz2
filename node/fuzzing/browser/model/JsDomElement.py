# coding=utf8
import random
from JsObject import JsObject
from JsDocument import JsDocument
from values import FuzzValues


class JsDomElement(JsObject):
    TYPE = "JsElement"

    def __init__(self, var_name, html_type=None, children=None):
        JsObject.__init__(self, var_name)
        self.__registered_events = {}
        self.__children = [] if not children else children
        self.__attributes = {}
        self.__html_type = html_type
        js_element_methods_and_properties = {'addEventListener': {'ret_val': None, 'parameters': ['EVENT', 'JS_EVENT_LISTENER'], 'method': self.addEventListener},
                                             'appendChild': {'ret_val': None, 'parameters': ['JS_DOM_ELEMENT'], 'method': self.appendChild},
                                             'blur': {'ret_val': None, 'parameters': None, 'method': self.blur},
                                             'click': {'ret_val': None, 'parameters': None, 'method': self.click},
                                             'cloneNode': {'ret_val': 'JS_DOM_ELEMENT', 'parameters': ['BOOL'], 'method': self.cloneNode}, #  TODO: parameters
                                             'compareDocumentPosition': {'ret_val': 'INT', 'parameters': ['JS_DOM_ELEMENT'], 'method': self.compareDocumentPosition},
                                             'focus': {'ret_val': None, 'parameters': None, 'method': self.focus},
                                             'getAttribute': {'ret_val': 'HTML_ATTR_VAL', 'parameters': ['HTML_ATTR'], 'method': self.getAttribute},
                                             'getAttributeNode': {'ret_val': 'JS_ATTR', 'parameters': ['HTML_ATTR'], 'method': self.getAttributeNode},
                                             'getElementsByClassName': {'ret_val': 'JS_NODE_LIST', 'parameters': ['CLASS_NAME'], 'method': self.getElementsByClassName},
                                             'getElementsByTagName': {'ret_val': 'JS_NODE_LIST', 'parameters': ['HTML_TAG'], 'method': self.getElementsByTagName},
                                             #'getFeature': {'ret_val': 0, 'parameters': None, 'method': self.getFeature},
                                             #'getUserData': {'ret_val': 0, 'parameters': None, 'method': self.getUserData},
                                             'hasAttribute': {'ret_val': 'BOOL', 'parameters': ['HTML_ATTR'], 'method': self.hasAttribute},
                                             'hasAttributes': {'ret_val': 'BOOL', 'parameters': None, 'method': self.hasAttributes},
                                             'hasChildNodes': {'ret_val': 'BOOL', 'parameters': None, 'method': self.hasChildNodes},
                                             'insertBefore': {'ret_val': 'JS_DOM_ELEMENT', 'parameters': ['JS_DOM_ELEMENT', 'JS_DOM_ELEMENT'], 'method': self.insertBefore},
                                             'isDefaultNamespace': {'ret_val': 'BOOL', 'parameters': None, 'method': self.isDefaultNamespace},
                                             'isEqualNode': {'ret_val': 'BOOL', 'parameters': ['JS_DOM_ELEMENT'], 'method': self.isEqualNode},
                                             'isSameNode': {'ret_val': 'BOOL', 'parameters': ['JS_DOM_ELEMENT'], 'method': self.isSameNode},
                                             #'isSupported': {'ret_val': 0, 'parameters': 0, 'method': self.isSupported},
                                             'normalize': {'ret_val': None, 'parameters': None, 'method': self.normalize},
                                             'querySelector': {'ret_val': 'JS_DOM_ELEMENT', 'parameters': ['CSS_SELECTOR'], 'method': self.querySelector},
                                             'querySelectorAll': {'ret_val': 'JS_NODE_LIST', 'parameters': ['CSS_SELECTOR'], 'method': self.querySelectorAll},
                                             'removeAttribute': {'ret_val': None, 'parameters': ['HTML_ATTR'], 'method': self.removeAttribute},
                                             'removeChild': {'ret_val': 'JS_DOM_ELEMENT', 'parameters': ['JS_DOM_CHILD_ELEMENT'], 'method': self.removeChild},
                                             'replaceChild': {'ret_val': 'JS_DOM_ELEMENT', 'parameters': ['JS_DOM_ELEMENT', 'JS_DOM_CHILD_ELEMENT'], 'method': self.replaceChild},
                                             'removeEventListener': {'ret_val': None, 'parameters': ['EVENT', 'JS_EVENT_LISTENER'], 'method': self.removeEventListener},
                                             'select': {'ret_val': None, 'parameters': None, 'method': self.select},
                                             'setAttribute': {'ret_val': None, 'parameters': ['HTML_ATTR', 'HTML_ATTR_VAL'], 'method': self.setAttribute},
                                             #'setUserData': {'ret_val': 0, 'parameters': 0, 'method': self.setUserData},
                                             #'item': {'ret_val': 0, 'parameters': 0, 'method': self.item},
                                             # -------------------------- PROPERTIES -----------------------------------
                                             #  TODO: think about how to change PROPERTIES ....
                                             # -------------------------------------------------------------------------
                                             'accessKey': {'ret_val': 'JS_STRING', 'parameters': None, 'method': self.accessKey},
                                             'attributes_prop': {'ret_val': 'JS_NODE_MAP', 'parameters': None, 'method': self.attributes_prop},
                                             'childNodes': {'ret_val': 'JS_NODE_LIST', 'parameters': None, 'method': self.childNodes},
                                             'className': {'ret_val': 'JS_STRING', 'parameters': ['JS_STRING*'], 'method': self.className},
                                             'clientHeight': {'ret_val': 'INT', 'parameters': None, 'method': self.clientHeight},
                                             'clientWidth': {'ret_val': 'INT', 'parameters': None, 'method': self.clientWidth},
                                             'contentEditable': {'ret_val': 'BOOL', 'parameters': None, 'method': self.contentEditable},
                                             'dir': {'ret_val': 'TEXT_DIRECTION', 'parameters': ['TEXT_DIRECTION*'], 'method': self.dir},
                                             'firstChild': {'ret_val': 'JS_DOM_ELEMENT', 'parameters': None, 'method': self.firstChild},
                                             'id': {'ret_val': 'JS_IDENTIFIER', 'parameters': None, 'method': self.id},
                                             'innerHtml': {'ret_val': 'HTML_CODE', 'parameters': ['HTML_CODE*'], 'method': self.innerHtml},
                                             'isContentEditable': {'ret_val': 'BOOL', 'parameters': None, 'method': self.isContentEditable},
                                             'lang': {'ret_val': 'LANG', 'parameters': ['LANG_CODE*'], 'method': self.lang},
                                             'lastChild': {'ret_val': 'JS_DOM_ELEMENT', 'parameters': None, 'method': self.lastChild},
                                             'namespaceURI': {'ret_val': 'NAMESPACE_URI', 'parameters': None, 'method': self.namespaceURI},
                                             'nodeName': {'ret_val': 'JS_STRING', 'parameters': None, 'method': self.nodeName},
                                             'nextSibling': {'ret_val': 'JS_DOM_ELEMENT', 'parameters': None, 'method': self.nextSibling},
                                             'nodeType': {'ret_val': 'INT', 'parameters': None, 'method': self.nodeType},
                                             'nodeValue': {'ret_val': 'JS_STRING', 'parameters': ['JS_STRING*'], 'method': self.nodeValue},
                                             'offsetHeight': {'ret_val': 'INT', 'parameters': None, 'method': self.offsetHeight},
                                             'offsetWidth': {'ret_val': 'INT', 'parameters': None, 'method': self.offsetWidth},
                                             'offsetLeft': {'ret_val': 'INT', 'parameters': None, 'method': self.offsetLeft},
                                             'offsetParent': {'ret_val': 'INT', 'parameters': None, 'method': self.offsetParent},
                                             'offsetTop': {'ret_val': 'INT', 'parameters': None, 'method': self.offsetTop},
                                             #'ownerDocument': {'ret_val': 'JS_DOCUMENT', 'parameters': None, 'method': self.ownerDocument},
                                             'parentNode': {'ret_val': 'JS_DOM_ELEMENT', 'parameters': None, 'method': self.parentNode},
                                             'previousSibling': {'ret_val': 'JS_DOM_ELEMENT', 'parameters': None, 'method': self.previousSibling},
                                             'scrollHeight': {'ret_val': 'INT', 'parameters': None, 'method': self.scrollHeight},
                                             'scrollLeft': {'ret_val': 'INT', 'parameters': None, 'method': self.scrollLeft},
                                             'scrollTop': {'ret_val': 'INT', 'parameters': None, 'method': self.scrollTop},
                                             'scrollWidth': {'ret_val': 'INT', 'parameters': None, 'method': self.scrollWidth},
                                             'style': {'ret_val': 'CSS_STYLE', 'parameters': ['CSS_STYLE*'], 'method': self.style},
                                             'tabIndex': {'ret_val': 'INT', 'parameters': ['INT*'], 'method': self.tabIndex},
                                             'tagName': {'ret_val': 'HTML_TAG', 'parameters': None, 'method': self.tagName},
                                             'textContent': {'ret_val': 'JS_STRING', 'parameters': ['JS_STRING*'], 'method': self.textContent},
                                             'title': {'ret_val': 'JS_STRING', 'parameters': ['JS_STRING*'], 'method': self.title},

                                             }
        self._methods_and_properties.update(js_element_methods_and_properties)

    @property
    def registered_events(self):
        return self.__registered_events

    def get_children(self):
        return self.__children

    def set_children(self, children):
        self.__children = children

    @property
    def html_type(self):
        return self.__html_type

    @property
    def attributes(self):
        return self.__attributes

    def get_event_trigger(self, event):
        if event == 'click':
            return self.click()
        elif event == 'error':
            code = "var error_event  = new ErrorEvent();"
            code += self.dispatchEvent("error_event") + ";"
            return code
        elif event == 'load':
            return ""
        elif event == 'scroll':
            return self.scrollTop() + ";"
        elif event == 'resize':
            return ""
        elif event == 'change':
            return ""
        elif event == 'focus':
            return self.focus() + ";"
        elif event == 'focusin':
            return self.focus() + ";"
        elif event == 'blur':
            return self.blur() + ";"
        elif event == 'select':
            return self.select() + ";"
        elif event == 'pageshow':
            return ""
        elif event == 'unload':
            return ""
        elif event == 'beforeunload':
            return ""
        elif event == 'DOMAttrModified':
            return ""  #  self.setAttribute(random.choice(self.attributes), random.choice(FuzzValues.INTERESTING_VALUES)) + ";\n"
        elif event == 'DOMAttributeNameChanged':
            return ""
        elif event == 'DOMCharacterDataModified':
            return ""
        elif event == 'DOMElementNameChanged':
            return self.setAttribute("name", "\"" + random.choice(FuzzValues.STRINGS) + "\"") + ";"
        elif event == 'DOMNodeInserted':
            return ""
        elif event == 'DOMNodeRemoved':
            return ""
        elif event == 'DOMNodeRemovedFromDocument':
            return ""
        elif event == 'DOMSubtreeModified':
            return ""
        else:
            return ""

# region METHODS
    def newElement(self):
        return self._name + " = " + JsDocument.createElement(self.__html_type)

    def newBodyElement(self):
        return self._name + " = " + JsDocument.prop_body() + ".createElement(" + self.__html_type + ")"

    def addEventListener(self, event, function):
        self.__registered_events[event] = function
        return self._name + ".addEventListener('" + event + "', " + function + ")"

    def appendChild(self, child_node):
        self.__children.append(child_node)
        return self._name + ".appendChild(" + child_node + ")"

    def blur(self):
        return self._name + ".blur()"

    def click(self):
        return self._name + ".click()"

    def cloneNode(self, deep):
        return self._name + ".cloneNode(" + str(deep).lower() + ")"

    def compareDocumentPosition(self, element):
        return self._name + ".compareDocumentPosition(" + element + ")"

    def focus(self):
        return self._name + ".focus()"

    def getAttribute(self, attr_name):
        return self._name + ".getAttribute('" + attr_name + "')"

    def getAttributeNode(self, attr_name):
        return self._name + ".getAttributeNode('" + attr_name + "')"

    def getElementsByClassName(self, class_name):
        return self._name + ".getElementsByClassName('" + class_name + "')"

    def getElementsByTagName(self, tag_name):
        return self._name + ".getElementsByTagName('" + tag_name + "')"

    def getFeature(self):
        return self._name + ".getFeature()"

    def getUserData(self):
        return self._name + ".getUserData()"

    def hasAttribute(self, attr_name):
        return self._name + ".hasAttribute('" + attr_name + "')"

    def hasAttributes(self):
        return self._name + ".hasAttributes()"

    def hasChildNodes(self):
        return self._name + ".hasChildNodes()"

    def insertBefore(self, new_element, child_element):
        return self._name + ".insertBefore(" + new_element + ", " + child_element + ")"

    def isDefaultNamespace(self):
        return self._name + ".isDefaultNamespace()"

    def isEqualNode(self, node):
        return self._name + ".isEqualNode(" + node + ")"

    def isSameNode(self, node):
        return self._name + ".isSameNode(" + node + ")"

    def isSupported(self, feature, version):
        return self._name + ".isSupported('" + feature + "', '" + version + ")"

    def normalize(self):
        return self._name + ".normalize()"

    def querySelector(self, html_class_name):
        return self._name + ".querySelector('." + html_class_name + "')"

    def querySelectorAll(self, html_class_name):
        return self._name + ".querySelectorAll('." + html_class_name + "')"

    def removeAttribute(self, attr):
        if attr in self.__attributes.keys():
            del self.__attributes[attr]
        return self._name + ".removeAttribute('" + attr + "')"

    def removeChild(self, child_node):
        if self.__children.count(child_node) != 0:
            self.__children.remove(child_node)
        return self._name + ".removeChild(" + child_node + ")"

    def replaceChild(self, new_node, child_node):
        if self.__children.count(child_node) != 0:
            self.__children.remove(child_node)
            self.__children.append(new_node)
        return self._name + ".replaceChild(" + new_node + ", " + child_node + ")"

    def removeEventListener(self, event, function):
        if event in self.__registered_events.keys():
            del self.__registered_events[event]
        return self._name + ".removeEventListener('" + event + "', " + function + ")"

    def select(self):
        return self._name + ".select()"

    def setAttribute(self, attr_name, attr_value):
        self.__attributes[attr_name] = attr_value
        return self._name + ".setAttribute('" + attr_name + "', " + attr_value + ")"

    def setAttributeNode(self, attr):
        return self._name + ".setAtrributeNode(" + attr + ")"

    def setUserData(self, data):
        return self._name + ".setUserData(" + data + ")"

#    def toString(self):
#        return self._name + ".toString()"

    def item(self, index):
        return self._name + ".item(" + index + ")"
# endregion

# region PROPERTIES
    def accessKey(self):
        return self._name + ".accessKey"

    def attributes_prop(self):
        return self._name + ".attributes"

    def childNodes(self):
        return self._name + ".childNodes"

    def className(self, class_name=None):
        return self._name + ".className" if class_name is None else self._name + ".className = " + class_name

    def clientHeight(self):
        return self._name + ".clientHeight"

    def clientWidth(self):
        return self._name + ".clientWidth"

    def contentEditable(self):
        return self._name + ".contentEditable"

    def dir(self, text_dir=None):
        return self._name + ".dir" if text_dir is None else self._name + ".dir = " + text_dir

    def firstChild(self):
        return self._name + ".firstChild"

    def id(self):
        return self._name + ".id"

    def innerHtml(self, html_code=None):
        return self._name + ".innerHTML" if html_code is None else self._name + ".innerHtml = " + html_code

    def isContentEditable(self):
        return self._name + ".isContentEditable"

    def lang(self, lang_code=None):
        return self._name + ".lang" if lang_code is None else self._name + ".lang = " + lang_code

    def lastChild(self):
        return self._name + ".lastChild"

    def namespaceURI(self):
        return self._name + ".namespaceURI"

    def nextSibling(self):
        return self._name + ".nextSibling"

    def nodeName(self):
        return self._name + ".nodeName"

    def nodeType(self):
        return self._name + ".nodeType"

    def nodeValue(self, value=None):
        return self._name + ".nodeValue" if value is None else self._name + ".nodeValue = " + value

    def offsetHeight(self):
        return self._name + ".offsetHeight"

    def offsetWidth(self):
        return self._name + ".offsetWidth"

    def offsetLeft(self):
        return self._name + ".offsetLeft"

    def offsetParent(self):
        return self._name + ".offsetParent"

    def offsetTop(self):
        return self._name + ".offsetTop"

    def ownerDocument(self):
        return self._name + ".ownerDocument"

    def parentNode(self):
        return self._name + ".parentNode"

    def previousSibling(self):
        return self._name + ".previousSibling"

    def scrollHeight(self):
        return self._name + ".scrollHeight"

    def scrollLeft(self):
        return self._name + ".scrollLeft"

    def scrollTop(self):
        return self._name + ".scrollTop"

    def scrollWidth(self):
        return self._name + ".scrollWidth"

    def style(self, style=None):
        return self._name + ".style" if style is None else self._name + ".style." + style[0] + " = " + style[1]

    def tabIndex(self, tab_index=None):
        return self._name + ".tabIndex" if tab_index is None else self._name + ".tabIndex = " + str(tab_index)

    def tagName(self):
        return self._name + ".tagName"

    def textContent(self, text_content=None):
        return self._name + ".textContent" if text_content is None else self._name + ".textContent = " + text_content

    def title(self, title=None):
        return self._name + ".title" if title is None else self._name + ".title = " + title

    def dispatchEvent(self, event):
        return self._name + ".dipatchEvent(" + event + ")"
# endregion
