__author__ = 'susperius'
import html
from node.config import ConfigParser

class WebSite:
    def __init__(self):
        self._funcs = ['home', 'node_detail']
        self._statuses = {200: '200 OK', 404: '404 FILE NOT FOUND'}
        self._header_html = [('Content-Type', 'text/html')]
        self._header_css = [('Content-Type', 'text/css')]
        with open("web/index.html", 'r') as fd:
            self._html_template = fd.read()

    @property
    def funcs(self):
        return self._funcs

    def home(self, nodes):
        home_html = self._html_template
        overview_table = html.TABLE_HEADER
        table_caption = ""
        table_caption_list = ["NODE NAME", "NODE ADDRESS", "CRASHES", "STATUS", "LAST CONTACT"]
        for element in table_caption_list:
            table_caption += html.TABLE_HEAD_CAPTION.replace("CONTENTS", element)
        table_caption = html.TABLE_ELEMENT.replace("CONTENTS", table_caption)
        node_table = ""
        for key in nodes.keys():
            node_name = html.NODE_LINK.replace("CONTENTS", nodes[key].name)
            node_name = node_name.replace("NAME", nodes[key].address)
            node = html.TABLE_DEFAULT_CONTENT.replace("CONTENTS", node_name) + \
                   html.TABLE_DEFAULT_CONTENT.replace("CONTENTS", nodes[key].address) + \
                   html.TABLE_DEFAULT_CONTENT.replace("CONTENTS", str(nodes[key].crashes)) + \
                   html.TABLE_DEFAULT_CONTENT.replace("CONTENTS", "Active" if nodes[key].status else "Inactive") + \
                   html.TABLE_DEFAULT_CONTENT.replace("CONTENTS", nodes[key].last_contact)
            node_table += html.TABLE_ELEMENT.replace("CONTENTS", node)
        overview_table += table_caption + node_table + html.TABLE_FOOTER
        home_html = home_html.replace("SECTION_TITLE", "OVERVIEW")
        home_html = home_html.replace("REPLACE_ME", "<b>PyFuzz 2 Nodes</b><br>" + overview_table)
        return self._statuses[200], self._header_html, home_html

    def node_detail(self, node):
        node_config = node.info
        from_conf_file = ConfigParser(node.config)
        node_config += from_conf_file.dump_additional_information()
        node_detail_html = self._html_template
        node_detail_html = node_detail_html.replace("SECTION_TITLE", node.name)
        nodes = html.FORM_HEADER.replace("ATTRIBS", "action=\"/index.py?func=node_detail&node=" +
                                         node.address + "&submit=1\" method=\"post\"") + html.TABLE_HEADER
        nodes += html.TABLE_ELEMENT.replace("CONTENTS", html.TABLE_HEAD_CAPTION.replace("CONTENTS", "") +
                                            html.TABLE_HEAD_CAPTION.replace("CONTENTS", ""))
        for i in range(4):
            nodes += html.TABLE_ELEMENT.replace("CONTENTS", html.TABLE_DEFAULT_CONTENT.replace("CONTENTS",
                                                        html.BOLD.replace("CONTENTS", node_config[i][0])) + \
                    html.TABLE_DEFAULT_CONTENT.replace("CONTENTS", node_config[i][1]))
        del node_config[0:4]
        for elem in node_config:
            single_node = html.TABLE_DEFAULT_CONTENT.replace("CONTENTS", html.BOLD.replace("CONTENTS", elem[0]+": ")) + \
                     html.TABLE_DEFAULT_CONTENT.replace("CONTENTS",
                                                        html.INPUT_TEXT.replace("NAME",
                                                                                elem[0].lower()).replace("CONTENTS",
                                                                              elem[1]).replace("ATTRIBS", "size=\"60\""))
            nodes += html.TABLE_ELEMENT.replace("CONTENTS", single_node)
        nodes += html.TABLE_FOOTER + html.INPUT_SUBMIT + html.FORM_FOOTER
        nodes += html.FORM_HEADER.replace("ATTRIBS",
                                          "action=\"/index.py?func=home&reboot=" + node.address + "\" method=\"post\"") + \
            html.INPUT_SUBMIT.replace("Submit", "Reset Node") + html.FORM_FOOTER
        node_detail_html = node_detail_html.replace("REPLACE_ME", nodes)
        return self._statuses[200], self._header_html, node_detail_html

    def file_not_found(self):
        return self._statuses[404], self._header_html, ['<b>404 FILE NOT FOUND!</b>\n']

    def get_style(self):
        with open("web/style.css", 'r') as fd:
            style_css = fd.read()
        return self._statuses[200], self._header_css, style_css
