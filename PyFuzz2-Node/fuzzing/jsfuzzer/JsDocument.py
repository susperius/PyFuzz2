# coding=utf8
__author__ = "susperius"


class JsDocument:
    @staticmethod
    def addEventListener(event):
        return "document.addEventListener('" + event + "');\n"

    '''
    Variable zu node muss übergeben werden
    '''

    @staticmethod
    def adoptNode(node):
        return "document.adoptNode(" + node + ");\n"

    @staticmethod
    def close():
        return "document.close();\n"

    @staticmethod
    def createAttribute(attribute):
        return "document.createAttribute('" + attribute + "');\n"

    @staticmethod
    def createComment(comment):
        return "document.createComement('" + comment + "');\n"

    @staticmethod
    def createDocumentFragment(doc_frag):
        return "document.createDocumentFragment('" + doc_frag + "');\n"

    @staticmethod
    def createElement(element):
        return "document.createElement('" + element + "');\n"

    @staticmethod
    def createTextNode(text):
        return "document.createTextNode('" + text + "');\n"

    @staticmethod
    def getElementById(identifier):
        return "document.getElementById('" + identifier + "');\n"

    @staticmethod
    def getElementsByClassName(class_name):
        return "document.getElementsByClassName('" + class_name + "');\n"

    @staticmethod
    def getElementsByName(name):
        return "document.getElementsByName('" + name + "');\n"

    @staticmethod
    def getElementsByTagName(tag_name):
        return "document.getElementsByTagName('" + tag_name + "');\n"

    '''
    Variable zu node muss übergeben werden
    '''

    @staticmethod
    def importNode(node, deep):
        return "document.importNode(" + node + ", " + deep + ");\n"

    @staticmethod
    def normalize():
        return "document.normalize();\n"

    @staticmethod
    def normalizeDocument():
        return "document.normalizeDocument();\n"

    @staticmethod
    def open():
        return "document.open();\n"

    @staticmethod
    def querySelector(class_name):
        return "document.querySelector('" + class_name + "');\n"

    @staticmethod
    def querySelectorAll(class_name):
        return "document.querySelectorAll('" + class_name + "');\n"

    @staticmethod
    def removeEventListener(event_name, function_name):
        return "document.removeEventListener('" + event_name + "', " + function_name + ");\n"

    @staticmethod
    def renameNode(node, node_name, namespace_uri=None):
        if node == None:
            return "document.renameNode(" + node + ", null, '" + node_name + "');\n"
        else:
            return "document.renameNode(" + node + ", '" + namespace_uri + "', '" + node_name + "');\n"

    @staticmethod
    def write(text):
        return "document.write('" + text + "');\n"

    @staticmethod
    def writeln(test):
        return "document.writeln('" + text + "');\n"

    @staticmethod
    def prop_anchors():
        return "document.anchors"

    @staticmethod
    def prop_applets():
        return "document.applets"

    @staticmethod
    def prop_baseURI():
        return "document.baseURI"

    @staticmethod
    def prop_body():
        return "document.body"

    @staticmethod
    def prop_cookie():
        return "document.cookie"

    @staticmethod
    def prop_doctype():
        return "docuement.doctype"

    @staticmethod
    def prop_documentElement():
        return "document.documentElement"

    @staticmethod
    def prop_documentMode():
        return "document.documentMode"

    @staticmethod
    def prop_documentURI():
        return "document.documentURI"

    @staticmethod
    def prop_domain():
        return "document.domain"

    @staticmethod
    def prop_embeds():
        return "document.embeds"

    @staticmethod
    def prop_forms():
        return "document.forms"

    @staticmethod
    def prop_head():
        return "document.head"

    @staticmethod
    def prop_images():
        return "document.images"

    @staticmethod
    def prop_implementation():
        return "document.implementation"

    @staticmethod
    def prop_inputEncoding():
        return "document.inputEncoding"

    @staticmethod
    def prop_lastModified():
        return "document.lastModified"

    @staticmethod
    def prop_links():
        return "document.links"

    @staticmethod
    def prop_readyState():
        return "document.readyState"

    @staticmethod
    def prop_referrer():
        return "document.referrer"

    @staticmethod
    def prop_scripts():
        return "document.scripts"

    @staticmethod
    def prop_strictErrorChecking():
        return "document.strictErrorChecking"

    @staticmethod
    def prop_title():
        return "document.title"

    @staticmethod
    def prop_URL():
        return "document.URL"

