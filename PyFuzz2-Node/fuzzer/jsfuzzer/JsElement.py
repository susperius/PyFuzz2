# coding=utf8

class JsElement:
    def __init__(self, var_name):
        self.__name = var_name

    def addEventListener(self, event, function):
        return self.__name + ".addEventListener('" + event + "', " + function + ");\n"

    def appendChild(self, child_node):
        return self.__name + ".appendChild(" + child_node + ");\n"

    def blur(self):
        return self.__name + ".blur();\n"

    def click(self):
        return self.__name + ".click();\n"

    def cloneNode(self, deep):
        return self.__name + ".cloneNode(" + deep + ");\n"

    def compareDocumentPosition(self, element):
        return self.__name + ".compareDocumentPosition(" + element + ");\n"

    def focus(self):
        return self.__name + ".focus();\n"

    def getAttribute(self, attr_name):
        return self.__name + ".getAttribute('" + attr_name + "');\n"

    def getAttributeNode(self, attr_name):
        return self.__name + ".getAttributeNode('" + attr_name + "');\n"

    def getElementsByClassName(self, class_name):
        return self.__name + ".getElementsByClassName('" + class_name + "');\n"

    def getElementsByTagName(self, tag_name):
        return self.__name + ".getElementsByTagName('" + tag_name + "');\n"

    def getFeature(self):
        return self.__name + ".getFeature();\n"

    def getUserData(self):
        return self.__name + ".getUserData();\n"

    def hasAttribute(self, attr_name):
        return self.__name + ".hasAttribute('" + attr_name + "');\n"

    def hasAttributes(self):
        return self.__name + ".hasAttributes();\n"

    def hasChildNodes(self):
        return self.__name + ".hasChildNodes();\n"

    def insertBefore(self, new_element, child_element):
        return self.__name + ".insertBefore(" + new_element + ", " + child_element + ");\n"

    def isDefaultNamespace(self):
        return self.__name + ".isDefaultNamespace();\n"

    def isEqualNode(self, node):
        return self.__name + ".isEqualNode(" + node + ");\n"

    def isSameNode(self, node):
        return self.__name + ".isSameNode(" + node + ");\n"

    def isSupported(self, feature, version):
        return self.__name + ".isSupported('" + feature + "', '" + version + ");\n"

    def normalize(self):
        return self.__name + ".normalize();\n"

    def querySelector(self, html_class_name):
        return self.__name + ".querySelector('." + html_class_name + "');\n"

    def querySelectorAll(self, html_class_name):
        return self.__name + ".querySelectorAll('." + html_class_name + "');\n"

    def removeAttribute(self, attr):
        return self.__name + ".removeAttribute('" + attr + "');\n"

    def removeChild(self, child_node):
        return self.__name + ".removeChild(" + child_node + ");\n"

    def replaceChild(self, new_node, child_node):
        return self.__name + ".replaceChild(" + new_node + ", " + child_node + ");\n"

    def removeEventListener(self, event, function):
        return self.__name + ".removeEventListener('" + event + "', " + function + ");\n"

    def setAttribute(self, attr_name, attr_value):
        return self.__name + ".setAttribute('" + attr_name + "', '" + attr_value + "');\n"

    def setAttributeNode(self, attr):
        return self.__name + ".setAtrributeNode(" + attr + ");\n"

    def setUserData(self, data):
        return self.__name + ".setUserData(" + data + ");\n"

    def toString(self):
        return self.__name + ".toString();\n"

    def item(self, index):
        return self.__name + ".item(" + index + ");\n"

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

