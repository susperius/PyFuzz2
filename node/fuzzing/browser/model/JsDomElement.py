# coding=utf8
from JsObject import JsObject


class JsDomElement(JsObject):
    TYPE = "JsElement"

    def __init__(self, var_name, html_type):
        JsObject.__init__(self, var_name)
        self.__name = var_name
        self.__registered_events = {}
        self.__children = []
        self.__attributes = {}
        self.__html_type = html_type
        js_element_methods_and_properties = {'addEventListener': {'ret_val': None, 'parameters': ['JS_EVENT_LISTENER'], 'method': self.addEventListener},
                                             'appendChild': {'ret_val': None, 'parameters': ['JS_DOM_ELEMENT'], 'method': self.appendChild},
                                             'blur': {'ret_val': None, 'parameters': None, 'method': self.blur},
                                             'click': {'ret_val': None, 'parameters': None, 'method': self.click},
                                             'cloneNode': {'ret_val': 'JS_DOM_ELEMENT', 'parameters': 0, 'method': self.cloneNode}, #  TODO: parameters
                                             'compareDocumentPosition': {'ret_val': 0, 'parameters': 0, 'method': self.compareDocumentPosition},
                                             'focus': {'ret_val': 0, 'parameters': None, 'method': self.focus},
                                             'getAttribute': {'ret_val': 0, 'parameters': 0, 'method': self.getAttribute},
                                             'getAttributeNode': {'ret_val': 0, 'parameters': 0, 'method': self.getAttributeNode},
                                             'getElementsByClassName': {'ret_val': 0, 'parameters': 0, 'method': self.getElementsByClassName},
                                             'getElementsByTagName': {'ret_val': 0, 'parameters': 0, 'method': self.getElementsByTagName},
                                             'getFeature': {'ret_val': 0, 'parameters': None, 'method': self.getFeature},
                                             'getUserData': {'ret_val': 0, 'parameters': None, 'method': self.getUserData},
                                             'hasAttribute': {'ret_val': 0, 'parameters': ['HTML_ATTR'], 'method': self.hasAttribute},
                                             'hasAttributes': {'ret_val': 0, 'parameters': None, 'method': self.hasAttributes},
                                             'hasChildNodes': {'ret_val': 0, 'parameters': None, 'method': self.hasChildNodes},
                                             'insertBefore': {'ret_val': 0, 'parameters': ['JS_DOM_ELEMENT', 'JS_DOM_ELEMENT'], 'method': self.insertBefore},
                                             'isDefaultNamespace': {'ret_val': 0, 'parameters': None, 'method': self.isDefaultNamespace},
                                             'isEqualNode': {'ret_val': 0, 'parameters': ['JS_DOM_ELEMENT'], 'method': self.isEqualNode},
                                             'isSameNode': {'ret_val': 0, 'parameters': ['JS_DOM_ELEMENT'], 'method': self.isSameNode},
                                             'isSupported': {'ret_val': 0, 'parameters': 0, 'method': self.isSupported},
                                             'normalize': {'ret_val': 0, 'parameters': 0, 'method': self.normalize},
                                             'querySelector': {'ret_val': 0, 'parameters': 0, 'method': self.querySelector},
                                             'querySelectorAll': {'ret_val': 0, 'parameters': 0, 'method': self.querySelectorAll},
                                             'removeAttribute': {'ret_val': 0, 'parameters': ['HTML_ATTR'], 'method': self.removeAttribute},
                                             'removeChild': {'ret_val': 0, 'parameters': ['JS_DOM_CHILD_ELEMENT'], 'method': self.removeChild},
                                             'replaceChild': {'ret_val': 0, 'parameters': ['JS_DOM_ELEMENT', 'JS_DOM_CHILD_ELEMENT'], 'method': self.replaceChild},
                                             'removeEventListener': {'ret_val': 0, 'parameters': ['EVENT', 'JS_EVENT_LISTENER'], 'method': self.removeEventListener},
                                             'select': {'ret_val': None, 'parameters': None, 'method': self.select},
                                             'setAttribute': {'ret_val': 0, 'parameters': ['HTML_ATTR', 'HTML_ATTR_VAL'], 'method': self.setAttribute},
                                             'setUserData': {'ret_val': 0, 'parameters': 0, 'method': self.setUserData},
                                             'item': {'ret_val': 0, 'parameters': 0, 'method': self.item},
                                             # -------------------------- PROPERTIES -----------------------------------
                                             #  TODO: think about how to change PROPERTIES ....
                                             # -------------------------------------------------------------------------
                                             'accessKey': {'ret_val': 0, 'parameters': None, 'method': self.accessKey},
                                             'attributes_prop': {'ret_val': 0, 'parameters': None, 'method': self.attributes_prop},
                                             'childNodes': {'ret_val': 0, 'parameters': None, 'method': self.childNodes},
                                             'className': {'ret_val': 0, 'parameters': None, 'method': self.className},
                                             'clientHeight': {'ret_val': 0, 'parameters': None, 'method': self.clientHeight},
                                             'clientWidth': {'ret_val': 0, 'parameters': None, 'method': self.clientWidth},
                                             'contentEditable': {'ret_val': 0, 'parameters': None, 'method': self.contentEditable},
                                             'dir': {'ret_val': 0, 'parameters': None, 'method': self.dir},
                                             'firstChild': {'ret_val': 0, 'parameters': None, 'method': self.firstChild},
                                             'id': {'ret_val': 0, 'parameters': None, 'method': self.id},
                                             'innerHtml': {'ret_val': 0, 'parameters': None, 'method': self.innerHtml},
                                             'isContentEditable': {'ret_val': 0, 'parameters': 0, 'method': self.isContentEditable},
                                             'lang': {'ret_val': 0, 'parameters': 0, 'method': self.lang},
                                             'lastChild': {'ret_val': 'JS_DOM_ELEMENT', 'parameters': 0, 'method': self.lastChild},
                                             'namespaceURI': {'ret_val': 0, 'parameters': 0, 'method': self.namespaceURI},
                                             'nodeName': {'ret_val': 0, 'parameters': 0, 'method': self.nodeName},
                                             'nextSibling': {'ret_val': 0, 'parameters': 0, 'method': self.nextSibling},
                                             'nodeType': {'ret_val': 0, 'parameters': 0, 'method': self.nodeType},
                                             'nodeValue': {'ret_val': 0, 'parameters': 0, 'method': self.nodeValue},
                                             'offsetHeight': {'ret_val': 0, 'parameters': 0, 'method': self.offsetHeight},
                                             'offsetWidth': {'ret_val': 0, 'parameters': 0, 'method': self.offsetWidth},
                                             'offsetLeft': {'ret_val': 0, 'parameters': 0, 'method': self.offsetLeft},
                                             'offsetParent': {'ret_val': 0, 'parameters': 0, 'method': self.offsetParent},
                                             'offsetTop': {'ret_val': 0, 'parameters': 0, 'method': self.offsetTop},
                                             'ownerDocument': {'ret_val': 0, 'parameters': 0, 'method': self.ownerDocument},
                                             'parentNode': {'ret_val': 0, 'parameters': 0, 'method': self.parentNode},
                                             'previousSibling': {'ret_val': 0, 'parameters': 0, 'method': self.previousSibling},
                                             'scrollHeight': {'ret_val': 0, 'parameters': 0, 'method': self.scrollHeight},
                                             'scrollLeft': {'ret_val': 0, 'parameters': 0, 'method': self.scrollLeft},
                                             'scrollTop': {'ret_val': 0, 'parameters': 0, 'method': self.scrollTop},
                                             'scrollWidth': {'ret_val': 0, 'parameters': 0, 'method': self.scrollWidth},
                                             'style': {'ret_val': 0, 'parameters': 0, 'method': self.style},
                                             'tabIndex': {'ret_val': 0, 'parameters': 0, 'method': self.tabIndex},
                                             'tagName': {'ret_val': 0, 'parameters': 0, 'method': self.tagName},
                                             'textContent': {'ret_val': 0, 'parameters': 0, 'method': self.textContent},
                                             'title': {'ret_val': 0, 'parameters': 0, 'method': self.title},
                                             'length': {'ret_val': 0, 'parameters': 0, 'method': self.length}
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

# region METHODS
    def addEventListener(self, event, function):
        self.__registered_events[event] = function
        return self.__name + ".addEventListener('" + event + "', " + function + ");"

    def appendChild(self, child_node):
        self.__children.append(child_node)
        return self.__name + ".appendChild(" + child_node + ");"

    def blur(self):
        return self.__name + ".blur();"

    def click(self):
        return self.__name + ".click();"

    def cloneNode(self, deep):
        return self.__name + ".cloneNode(" + str(deep).lower() + ");"

    def compareDocumentPosition(self, element):
        return self.__name + ".compareDocumentPosition(" + element + ");"

    def focus(self):
        return self.__name + ".focus();"

    def getAttribute(self, attr_name):
        return self.__name + ".getAttribute('" + attr_name + "');"

    def getAttributeNode(self, attr_name):
        return self.__name + ".getAttributeNode('" + attr_name + "');"

    def getElementsByClassName(self, class_name):
        return self.__name + ".getElementsByClassName('" + class_name + "');"

    def getElementsByTagName(self, tag_name):
        return self.__name + ".getElementsByTagName('" + tag_name + "');"

    def getFeature(self):
        return self.__name + ".getFeature();"

    def getUserData(self):
        return self.__name + ".getUserData();"

    def hasAttribute(self, attr_name):
        return self.__name + ".hasAttribute('" + attr_name + "');"

    def hasAttributes(self):
        return self.__name + ".hasAttributes();"

    def hasChildNodes(self):
        return self.__name + ".hasChildNodes();"

    def insertBefore(self, new_element, child_element):
        return self.__name + ".insertBefore(" + new_element + ", " + child_element + ");"

    def isDefaultNamespace(self):
        return self.__name + ".isDefaultNamespace();"

    def isEqualNode(self, node):
        return self.__name + ".isEqualNode(" + node + ");"

    def isSameNode(self, node):
        return self.__name + ".isSameNode(" + node + ");"

    def isSupported(self, feature, version):
        return self.__name + ".isSupported('" + feature + "', '" + version + ");"

    def normalize(self):
        return self.__name + ".normalize();"

    def querySelector(self, html_class_name):
        return self.__name + ".querySelector('." + html_class_name + "');"

    def querySelectorAll(self, html_class_name):
        return self.__name + ".querySelectorAll('." + html_class_name + "');"

    def removeAttribute(self, attr):
        del self.__attributes[attr]
        return self.__name + ".removeAttribute('" + attr + "');"

    def removeChild(self, child_node):
        self.__children.remove(child_node)
        return self.__name + ".removeChild(" + child_node + ");"

    def replaceChild(self, new_node, child_node):
        self.__children.remove(child_node)
        self.__children.append(new_node)
        return self.__name + ".replaceChild(" + new_node + ", " + child_node + ");"

    def removeEventListener(self, event, function):
        del self.__registered_events[event]
        return self.__name + ".removeEventListener('" + event + "', " + function + ");"

    def select(self):
        return self.__name + ".select();"

    def setAttribute(self, attr_name, attr_value):
        self.__attributes[attr_name] = attr_value
        return self.__name + ".setAttribute('" + attr_name + "', '" + attr_value + "');"

    def setAttributeNode(self, attr):
        return self.__name + ".setAtrributeNode(" + attr + ");"

    def setUserData(self, data):
        return self.__name + ".setUserData(" + data + ");"

#    def toString(self):
#        return self.__name + ".toString();"

    def item(self, index):
        return self.__name + ".item(" + index + ");"
# endregion

# region PROPERTIES
    def accessKey(self):
        return self.__name + ".accessKey"

    def attributes_prop(self):
        return self.__name + ".attributes"

    def childNodes(self):
        return self.__name + ".childNodes"

    def className(self):
        return self.__name + ".className"

    def clientHeight(self):
        return self.__name + ".clientHeight"

    def clientWidth(self):
        return self.__name + ".clientWidth"

    def contentEditable(self):
        return self.__name + ".contentEditable"

    def dir(self):
        return self.__name + ".dir"

    def firstChild(self):
        return self.__name + ".firstChild"

    def id(self):
        return self.__name + ".id"

    def innerHtml(self):
        return self.__name + ".innerHTML"

    def isContentEditable(self):
        return self.__name + ".isContentEditable"

    def lang(self):
        return self.__name + ".lang"

    def lastChild(self):
        return self.__name + ".lastChild"

    def namespaceURI(self):
        return self.__name + ".namespaceURI"

    def nextSibling(self):
        return self.__name + ".nextSibling"

    def nodeName(self):
        return self.__name + ".nodeName"

    def nodeType(self):
        return self.__name + ".nodeType"

    def nodeValue(self):
        return self.__name + ".nodeValue"

    def offsetHeight(self):
        return self.__name + ".offsetHeight"

    def offsetWidth(self):
        return self.__name + ".offsetWidth"

    def offsetLeft(self):
        return self.__name + ".offsetLeft"

    def offsetParent(self):
        return self.__name + ".offsetParent"

    def offsetTop(self):
        return self.__name + ".offsetTop"

    def ownerDocument(self):
        return self.__name + ".ownerDocument"

    def parentNode(self):
        return self.__name + ".parentNode"

    def previousSibling(self):
        return self.__name + ".previousSibling"

    def scrollHeight(self):
        return self.__name + ".scrollHeight"

    def scrollLeft(self):
        return self.__name + ".scrollLeft"

    def scrollTop(self):
        return self.__name + ".scrollTop"

    def scrollWidth(self):
        return self.__name + ".scrollWidth"

    def style(self):
        return self.__name + ".style"

    def tabIndex(self):
        return self.__name + ".tabIndex"

    def tagName(self):
        return self.__name + ".tagName"

    def textContent(self):
        return self.__name + ".textContent"

    def title(self):
        return self.__name + ".title"

    def length(self):
        return self.__name + ".length"
# endregion
