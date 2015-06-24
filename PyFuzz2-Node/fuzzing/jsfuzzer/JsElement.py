# coding=utf8

class JsElement:
    def __init__(self, var_name):
        self.__name = var_name
        self.__registered_events = {}
        self.__children = []
        self.__attributes = {}

    @property
    def name(self):
        return self.__name

    @property
    def registered_events(self):
        return self.__registered_events

    def get_children(self):
        return self.__children

    def set_children(self, children):
        self.__children = children

    @property
    def attributes(self):
        return self.__attributes

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

    def setAttribute(self, attr_name, attr_value):
        self.__attributes[attr_name] = attr_value
        return self.__name + ".setAttribute('" + attr_name + "', '" + attr_value + "');"

    def setAttributeNode(self, attr):
        return self.__name + ".setAtrributeNode(" + attr + ");"

    def setUserData(self, data):
        return self.__name + ".setUserData(" + data + ");"

    def toString(self):
        return self.__name + ".toString();"

    def item(self, index):
        return self.__name + ".item(" + index + ");"

    # -----  PROPS ------
    def prop_accessKey(self):
        return self.__name + ".accessKey"

    def prop_attributes(self):
        return self.__name + ".attributes"

    def prop_childNodes(self):
        return self.__name + ".childNodes"

    def prop_className(self):
        return self.__name + ".className"

    def prop_clientHeight(self):
        return self.__name + ".clientHeight"

    def prop_clientWidth(self):
        return self.__name + ".clientWidth"

    def prop_contentEditable(self):
        return self.__name + ".contentEditable"

    def prop_dir(self):
        return self.__name + ".dir"

    def prop_firstChild(self):
        return self.__name + ".firstChild"

    def prop_id(self):
        return self.__name + ".id"

    def prop_innerHtml(self):
        return self.__name + ".innerHTML"

    def prop_isContentEditable(self):
        return self.__name + ".isContentEditable"

    def prop_lang(self):
        return self.__name + ".lang"

    def prop_lastChild(self):
        return self.__name + ".lastChild"

    def prop_namespaceURI(self):
        return self.__name + ".namespaceURI"

    def prop_nextSibling(self):
        return self.__name + ".nextSibling"

    def prop_nodeName(self):
        return self.__name + ".nodeName"

    def prop_nodeType(self):
        return self.__name + ".nodeType"

    def prop_nodeValue(self):
        return self.__name + ".nodeValue"

    def prop_offsetHeight(self):
        return self.__name + ".offsetHeight"

    def prop_offsetWidth(self):
        return self.__name + ".offsetWidth"

    def prop_offsetLeft(self):
        return self.__name + ".offsetLeft"

    def prop_offsetParent(self):
        return self.__name + ".offsetParent"

    def prop_offsetTop(self):
        return self.__name + ".offsetTop"

    def prop_ownerDocument(self):
        return self.__name + ".ownerDocument"

    def prop_parentNode(self):
        return self.__name + ".parentNode"

    def prop_previousSibling(self):
        return self.__name + ".previousSibling"

    def prop_scrollHeight(self):
        return self.__name + ".scrollHeight"

    def prop_scrollLeft(self):
        return self.__name + ".scrollLeft"

    def prop_scrollTop(self):
        return self.__name + ".scrollTop"

    def prop_scrollWidth(self):
        return self.__name + ".scrollWidth"

    def prop_style(self):
        return self.__name + ".style"

    def prop_tabIndex(self):
        return self.__name + ".tabIndex"

    def prop_tagName(self):
        return self.__name + ".tagName"

    def prop_textContent(self):
        return self.__name + ".textContent"

    def prop_title(self):
        return self.__name + ".title"

    def prop_length(self):
        return self.__name + ".length"

