__author__ = 'susperius'
import html
from node.model.config import ConfigParser
from node.fuzzing.fuzzers import FUZZERS

class WebSite:
    def __init__(self):
        self._funcs = ['home', 'node_detail']
        self._statuses = {200: '200 OK', 404: '404 FILE NOT FOUND'}
        self._header_html = [('Content-Type', 'text/html')]
        self._header_css = [('Content-Type', 'text/css')]
        self._header_js = [('Content-Type', 'application/javascript')]
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
        for key in sorted(nodes.keys()):
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
        add_config, fuzzer_conf = from_conf_file.dump_additional_information()
        node_config += add_config
        node_detail_html = self._html_template
        node_detail_html = node_detail_html.replace("SECTION_TITLE", node.name)
        node_conf_table = "<form action=\"/index.py?func=home&node=" + node.address + \
                          "&submit=1\" method=\"post\">\r\n" + "<table>\r\n"
        node_conf_table += "<tr><th/><th/></tr>\r\n"
        # General config settings
        for i in range(4):
            node_conf_table += "<tr>\r\n<td><b>" + node_config[i][0] + "</b></td>\r\n" + \
                               "<td>" + node_config[i][1] + "</td>\r\n</tr>\r\n"
        del node_config[0:4]
        for elem in node_config:
            single_node = "<td><b>" + elem[0] + "</b></td>\r\n" + \
                          "<td><input type=\"text\" name=\"" + elem[0].lower() + "\" value=\"" + \
                          elem[1] + "\" size=\"60\"></td>\r\n"
            node_conf_table += "<tr>\r\n" + single_node + "</tr>\r\n"
        node_conf_table += "</table>\r\n<table id=\"fuzz_table\" >\r\n<tr><th/><th/></tr>\r\n"
        # fuzzer settings
        fuzz_types_options = ""
        for key in FUZZERS.keys():
            fuzz_types_options += "<option>"+key+"</option>\r\n"
        node_conf_table += "<tr>\r\n<td><b>Fuzzer Type</b></td>\r\n<td><select id=\"fuzzers\" " + \
                           "onLoad=\"set_select_value('" + fuzzer_conf["fuzzer_type"] + "')\" " + \
                           " name=\"fuzzer_type\" onChange=\"changeFuzzer()\">\r\n" + \
                           fuzz_types_options+"</select>\r\n</td>\r\n</tr>\r\n"
        node_conf_table += "<div id=\"fuzz_config\">"
        for key in FUZZERS[fuzzer_conf["fuzzer_type"]]:
            node_conf_table += "<tr>\r\n<td><b>" + key + "</b></td>\r\n" + \
                               "<td><input type=\"text\" value=\"" + fuzzer_conf["fuzz_conf"][key] + "\" name=\"" + \
                               key + "\" >"
        # table end
        node_conf_table += "</div>"
        node_conf_table += "</table>\r\n<input type=\"submit\" value=\"Submit\">\r\n</form>\r\n"
        node_conf_table += "<form action=\"/index.py?func=home&reboot=" + node.address + "\" method=\"post\">\r\n" + \
                           "<input type=\"submit\" value=\"Reboot node\">\r\n</form>\r\n"
        node_detail_html = node_detail_html.replace("REPLACE_ME", node_conf_table)
        return self._statuses[200], self._header_html, node_detail_html

    def file_not_found(self):
        return self._statuses[404], self._header_html, ['<b>404 FILE NOT FOUND!</b>\n']

    @staticmethod
    def __get_file(file_name):
        with open(file_name, 'r') as fd:
            content = fd.read()
        return content

    def get_style(self):
        style_css = self.__get_file("web/style.css")
        return self._statuses[200], self._header_css, style_css

    def get_scripts(self):
        scripts = self.__get_file("web/scripts.js")
        fuzzers = "var fuzzers = [ "
        for key in FUZZERS.keys():
            fuzzers += "'" + key + "', [ "
            for elem in FUZZERS[key]:
                fuzzers += "'" + elem + "',"
            fuzzers = fuzzers[:-1]
            fuzzers += "],"
        fuzzers = fuzzers[:-1]
        fuzzers +="];\r\n"
        scripts = scripts.replace('FUZZERS', fuzzers)
        return self._statuses[200], self._header_js, scripts
