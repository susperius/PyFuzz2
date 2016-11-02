import os
from zipfile import ZipFile
from flask import Flask, render_template, send_file, abort, request
from table import SingleNodeTable, NodeTable, CrashTable
from gevent.queue import Queue
from model.web import WEB_QUEUE_TASKS
from model.database import DB_TYPES
from node.model.config import ConfigParser
from node.model.message_types import MESSAGE_TYPES
from model.database import SEPARATOR

#  TODO: Implement the stats and about sites
class WebInterface:
    def __init__(self, web_queue, node_dict, crash_dict):
        self._inc_confs = 0  # keep track of the actual open in and out going config files
        self._out_confs = 0
        self._web_queue = web_queue
        self._node_dict = node_dict
        self._crash_dict = crash_dict
        self.app = Flask(__name__)
        self.app.add_url_rule("/", "index", self.index_site)
        self.app.add_url_rule("/index.html", "index", self.index_site)
        self.app.add_url_rule("/stats.html", "stats", self.stats_site)
        self.app.add_url_rule("/about.html", "about", self.about_site)
        self.app.add_url_rule("/node/<string:addr>", 'node_detail', self.node_detail)
        self.app.add_url_rule("/node/<string:addr>/download", 'node_get_config', self.node_get_config)
        self.app.add_url_rule("/node/<string:addr>/upload", 'node_set_config', self.node_set_config, methods=['POST'])
        self.app.add_url_rule("/node/<string:addr>/reboot", 'node_reboot', self.node_reboot)
        self.app.add_url_rule("/node/<string:addr>/delete", 'node_delete', self.node_delete)
        self.app.add_url_rule("/crash/<string:program>/<string:descr>/<string:maj_hash>/download", 'download_crash',
                              self.download_crash)

    def index_site(self):
        table_items = []
        for node in self._node_dict.items():
            table_items.append(node[1].info)
        table_items.sort()
        node_table = NodeTable(table_items)
        return render_template("main.html", section_title="OVERVIEW", body_space=node_table)

    def stats_site(self):
        programs = {}
        for crashes in self._crash_dict.items():
            to_add = crashes[1].stats
            to_add['download'] = "click"
            to_add['program'] = crashes[1].program
            if crashes[1].program not in programs.keys():
                programs[crashes[1].program] = [to_add]
            else:
                programs[crashes[1].program].append(to_add)
        for key in programs.keys():
            programs[key] = CrashTable(programs[key])

        return render_template("stats.html", section_title="STATS", programs=programs)

    def about_site(self):
        return render_template("main.html", section_title="ABOUT")

    def node_detail(self, addr, msg=""):
        if addr not in self._node_dict.keys():
            abort(404)
        node = self._node_dict[addr]
        href_base = "/node/" + addr + "/"
        node_info_items = [{'descr': 'NAME', 'value': node.info['name']},
                           {'descr': 'IP ADDRESS', 'value': node.info['addr']},
                           {'descr': 'STATUS', 'value': node.info['status']},
                           {'descr': 'LAST CONTACT', 'value': node.info['last_contact']},
                           {'descr': 'CRASHES', 'value': node.info['crashes']}]
        node_info_table = SingleNodeTable(node_info_items)
        if node.config is not None:
            node_config = ConfigParser(node.config, True)
            general_config, programs, op_mode_conf = node_config.dump_additional_information()
            general_config_items = []
            for item in general_config:
                general_config_items.append({'descr': item[0], 'value': item[1]})
            count = 1
            program_items = []
            for prog in programs:
                program_items.append({'descr': 'Program ' + str(count), 'value': prog})
                count += 1
            op_mode_items = []
            if node_config.node_op_mode == "fuzzing":
                general_config_items.append({'descr': 'OP-Mode', 'value': "Fuzzing"})
                op_mode_items.append({'descr': 'Fuzzer Type', 'value': op_mode_conf['fuzzer_type']})
                for item in op_mode_conf['fuzz_conf'].items():
                    op_mode_items.append({'descr': item[0], 'value': item[1]})
            elif node.op_mode == "reducing":
                pass
            else:
                op_mode_items.append({'descr': 'OP-Mode', 'value': 'Not found'})
            general_config_table = SingleNodeTable(general_config_items)
            program_table = SingleNodeTable(program_items)
            op_mode_conf_table = SingleNodeTable(op_mode_items)
            return render_template("single_node.html", section_title="NODE DETAIL", node_info_table=node_info_table,
                                   general_config_table=general_config_table, program_table=program_table,
                                   op_mode_conf_table=op_mode_conf_table, href_base=href_base, message_from_server=msg)
        else:
            return render_template("single_node.html", section_title="NODE DETAIL", body_space=node_info_table,
                                   href_base=href_base, message_from_server=msg)

    def node_get_config(self, addr):
        if addr not in self._node_dict.keys():
            abort(404)
        else:
            path = "tmp/" + addr + "-out_conf.xml" if __name__ == "__main__" else "web/tmp/" + addr + "-out_conf.xml"
            node = self._node_dict[addr]
            if node.config is None:
                return self.node_detail(addr, msg="Config not found")
            else:
                with open(path, 'w+') as fd:
                    fd.write(node.config)
                return send_file(path.replace("web/", ""))  #  send file is using the path, where the app is located as cwd (seems like)

    def node_set_config(self, addr):
        if "conf_file" not in request.files or addr not in self._node_dict.keys():
            abort(404)
        path = "tmp/" + addr + "-inc_conf.xml" if __name__ == "__main__" else "web/tmp/" + addr + "-inc_conf.xml"
        node = self._node_dict[addr]
        rec_file = request.files['conf_file']
        rec_file.save(path)
        #  Check if it's a valid config
        message = "Config parsed successfully"
        error = False
        try:
            ConfigParser(path)
        except ValueError as v_err:
            message = "An error occured while parsing your config: " + v_err.message
            error = True
        except:
            message = "There was a general error with your configuration"
            error = True
        #  -----------------------------
        if not error:
            node.status = False
            with open(path) as fd:
                config = fd.read()
            self._web_queue.put((WEB_QUEUE_TASKS['TO_NODE'], [(addr, node.listener_port), MESSAGE_TYPES['SET_CONFIG'], config]))
        return self.node_detail(addr, message)

    def node_reboot(self, addr):
        if addr not in self._node_dict.keys():
            abort(404)
        node = self._node_dict[addr]
        node.status = False
        self._web_queue.put((WEB_QUEUE_TASKS['TO_NODE'], [(addr, node.listener_port), MESSAGE_TYPES['RESET'], ""]))
        return self.node_detail(addr)

    def node_delete(self, addr):
        if addr not in self._node_dict.keys():
            abort(404)
        self._web_queue.put((WEB_QUEUE_TASKS['TO_DB'], (DB_TYPES['DELETE_NODE'], addr)))
        del(self._node_dict[addr])
        return self.index_site()

    def download_crash(self, program, maj_hash, descr):
        if not self.__does_crash_exist(program, maj_hash, descr):
            abort(404)
        path = "results/" + program + "/" + descr + "/" + maj_hash + "/"
        zip_name = "CRASH-" + program + "-" + maj_hash + ".zip"
        upload_file = ZipFile("web/tmp/" + zip_name, "w")
        for root, dirs, files in os.walk(path):
            for act_file in files:
                upload_file.write(os.path.join(root, act_file))
        upload_file.close()
        return send_file("tmp/" + zip_name)

    def __does_crash_exist(self, program, maj_hash, descr):
        key = program + SEPARATOR + maj_hash
        if key in self._crash_dict.keys():
            if self._crash_dict[key].short_description == descr:
                return True
        return False

if __name__ == "__main__":
    from model.pyfuzz2_node import PyFuzz2Node
    node_dict = {}
    node_conf = ""
    with open("../node/node_config.xml") as fd:
        node_conf = fd.read()
    for i in range(10,30):
        new_node = PyFuzz2Node("NODE" + str(i), "192.168.1."+str(i), 31337)
        new_node.crashed(i)
        new_node.config = node_conf
        node_dict["192.168.1." + str(i)] = new_node
    intf = WebInterface(Queue(), node_dict, {})
    intf.app.run("127.0.0.1", 8080, debug=True)
