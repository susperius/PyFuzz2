from flask import Flask, render_template, send_file
from flask_table import Table, Col, LinkCol
from gevent.queue import Queue


class WebInterface:
    def __init__(self, web_queue, node_dict, crash_dict):
        self._web_queue = web_queue
        self._node_dict = node_dict
        self._crash_dict = crash_dict
        self.app = Flask(__name__)
        self.app.add_url_rule("/", "index", self.index_site)
        self.app.add_url_rule("/index.html", "index", self.index_site)
        self.app.add_url_rule("/stats.html", "stats", self.stats_site)
        self.app.add_url_rule("/about.html", "about", self.about_site)
        self.app.add_url_rule("/node/<string:addr>", 'single_node', self.single_node)

    def index_site(self):
        table_items = []
        for node in self._node_dict.items():
            table_items.append(node[1].info)
        table_items.sort()
        node_table = NodeTable(table_items)
        return render_template("index.html", section_title="OVERVIEW", body_space=node_table)

    def stats_site(self):
        return render_template("index.html", section_title="STATS")

    def about_site(self):
        return render_template("index.html", section_title="ABOUT")

    def single_node(self, addr):
        try:
            node = self._node_dict[addr]
        except KeyError:

            return render_template("index.html", section_title="NO SUCH NODE")
        node_name = node.name
        return render_template("index.html", section_title=node.name)


class NodeTable(Table):
    name = LinkCol("NODE NAME", "single_node", url_kwargs=dict(addr='addr'), attr='addr')
    addr = Col("NODE ADDRESS")
    crashes = Col("CRASHES")
    status = Col("STATUS")
    last_contact = Col("LAST CONTACT")


if __name__ == "__main__":
    from model.pyfuzz2_node import PyFuzz2Node
    node_dict = {}
    for i in range(10,30):
        new_node = PyFuzz2Node("NODE" + str(i), "192.168.1."+str(i), 31337)
        new_node.crashed(i)
        node_dict["192.168.1." + str(i)] = new_node
    intf = WebInterface(Queue(), node_dict, {})
    intf.app.run("127.0.0.1", 5000, debug=True)
