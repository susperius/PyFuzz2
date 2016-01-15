__author__ = 'susperius'
import html
import logging
from model.crash import Crash
from node.model.config import ConfigParser
from node.fuzzing.fuzzers import FUZZERS


class WebSite:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._funcs = ['home', 'node_detail', 'stats']
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
        table_caption_list = ["NODE NAME", "NODE ADDRESS", "CRASHES", "STATUS", "LAST CONTACT"]
        home_html = self._html_template
        overview_table = html.table_header(table_caption_list)
        node_table = ""
        for key in sorted(nodes.keys()):
            node_table += html.node_overview_node_entry(nodes[key].name, nodes[key].address, str(nodes[key].crashes),
                                                        "Active" if nodes[key].status else "Inactive",
                                                        nodes[key].last_contact)
        overview_table += node_table + html.table_footer()
        home_html = home_html.replace("SECTION_TITLE", "OVERVIEW")
        home_html = home_html.replace("REPLACE_ME", "<b>PyFuzz 2 Nodes</b><br>" + overview_table)
        return self._statuses[200], self._header_html, home_html

    def node_detail(self, node):
        node_config = node.info
        op_mode_conf = ""
        programs = None
        if node.config is not None:
            add_config, programs, op_mode_conf = ConfigParser(node.config, True).dump_additional_information()
            node_config += add_config
        node_detail_html = self._html_template
        node_detail_html = node_detail_html.replace("SECTION_TITLE", node.name)
        node_conf_table = "<form action=\"/index.py?func=home&node=" + node.address + \
                          "&submit=1\" method=\"post\">\r\n" + "<table>\r\n"
        node_conf_table += "<tr><th/>GENERAL CONFIG<th/></tr>\r\n"
        # ------------------------------------------------------------------------------------------------------------
        # General config settings
        for i in range(4):
            node_conf_table += html.node_detail_table_entry(node_config[i][0], node_config[i][1])
        del node_config[0:4]
        for elem in node_config:
            node_conf_table += html.node_detail_table_entry_editable(elem[0], elem[1])
        node_conf_table += "</table>\r\n<table id=\"programs_table\">\r\n"
        # ------------------------------------------------------------------------------------------------------------
        # Program settings
        if programs is not None:
            for i, prog in enumerate(programs):
                node_conf_table += "<tr><th>PROGRAM " + str(i) + "</th><th/></tr>\r\n"
                single_prog = ""
                for key, val in prog.items():
                    single_prog += html.node_detail_table_entry_editable(key, val, "prog-" + str(i) + " " + key)
                node_conf_table += single_prog
        node_conf_table += "</table>\r\n"
        # ------------------------------------------------------------------------------------------------------------
        # Fuzzer settings
        if op_mode_conf != "":
            node_conf_table += "<table id=\"fuzz_table\" >\r\n<tr><th>FUZZER SETTINGS</th><th/></tr>\r\n"
            fuzz_types_options = ""
            for key in FUZZERS.keys():
                fuzz_types_options += "<option>"+key+"</option>\r\n"
            node_conf_table += "<tr>\r\n<td><b>Fuzzer Type</b></td>\r\n<td><select id=\"fuzzers\" " + \
                               "onLoad=\"set_select_value('" + op_mode_conf["fuzzer_type"] + "')\" " + \
                               " name=\"fuzzer_type\" onChange=\"changeFuzzer()\">\r\n" + \
                               fuzz_types_options+"</select>\r\n</td>\r\n</tr>\r\n"
            for key in FUZZERS[op_mode_conf["fuzzer_type"]][0]:
                node_conf_table += html.node_detail_table_entry_editable(key, op_mode_conf['fuzz_conf'][key])
            node_conf_table += "</table>\r\n"
        else:
            node_conf_table += "<br><br><b>No additional information received by now</b>\r\n"
        node_conf_table += "<br>\r\n"
        node_conf_table += "<input type=\"submit\" value=\"Submit\" >\r\n</form>\r\n"
        node_conf_table += html.action_button("Reboot node", "/index.py?func=home&reboot=" + node.address,
                                              "post")
        node_conf_table += html.action_button("Delete node", "/index.py?func=home&del=" + node.address,
                                              "post")
        node_detail_html = node_detail_html.replace("REPLACE_ME", node_conf_table)
        return self._statuses[200], self._header_html, node_detail_html

    def stats(self, nodes_dict, crashes_dict):
        stats_html = self._html_template
        stats_html = stats_html.replace("SECTION_TITLE", "Crash Stats")
        stats_table = html.table_header(Crash.FIELDS, "stats_table")
        for key in sorted(crashes_dict.keys()):
            stats_table += html.table_entry(crashes_dict[key].stats)
        stats_table += html.table_footer()
        stats_html = stats_html.replace("REPLACE_ME", stats_table)
        return self._statuses[200], self._header_html, stats_html

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
            for elem in FUZZERS[key][0]:
                fuzzers += "'" + elem + "',"
            fuzzers = fuzzers[:-1]
            fuzzers += "],"
        fuzzers = fuzzers[:-1]
        fuzzers +="];\r\n"
        scripts = scripts.replace('FUZZERS', fuzzers)
        return self._statuses[200], self._header_js, scripts
