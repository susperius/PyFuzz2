__author__ = 'susperius'

import xml.etree.ElementTree as ET


class NodeConfig:
    def __init__(self, node_name="dummyNode", beacon_server="127.0.0.1", beacon_port="31337", report_server="127.0.0.1", report_port="32337", listener_port="32337"):
        self._tree = ET.parse("node_config.xml")
        self._root = self._tree.getroot()
        self._beacon = self._root.find("beacon")
        self._report = self._root.find("reporting")
        self._listener = self._root.find("listener")
        self._program = self._root.find("program")
        self._fuzzer = self._root.find("fuzzer")
        self.set_node_name(node_name)
        self.set_beacon_server(beacon_server)
        self.set_beacon_port(beacon_port)
        self.set_report_server(report_server)
        self.set_report_port(report_port)
        self.set_listener_port(listener_port)

    def set_node_name(self, name):
        self._root.attrib['name'] = name

    def set_beacon_port(self, port):
        self._beacon.attrib['port'] = str(port)

    def set_beacon_server(self, server):
        self._beacon.attrib['server'] = server

    def set_beacon_interval(self, interval):
        self._beacon.attrib['interval'] = interval

    def set_report_server(self, server):
        self._report.attrib['server'] = server

    def set_report_port(self, port):
        self._report.attrib['port'] = str(port)

    def set_listener_port(self, port):
        self._listener.attrib['port'] = str(port)

    def set_program_path(self, path):
        self._program.attrib['path'] = path

    def set_program_dbg_child(self, dbg_child):
        self._program.attrib['dbg_child'] = dbg_child

    def set_program_sleep_time(self, sleep_time):
        self._program.attrib['sleep_time'] = sleep_time

    def set_fuzzer(self, type, arg_dict):
        self._fuzzer.attrib['type'] = type
        for key in arg_dict.keys():
            self._fuzzer.attrib[key] = arg_dict[key]

    def dump(self):
        return ET.dump(self._tree)
