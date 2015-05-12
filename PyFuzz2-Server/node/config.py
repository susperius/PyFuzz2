__author__ = 'susperius'

import xml.etree.ElementTree as ET
import logging


class NodeConfig:
    def __init__(self, node_name="dummyNode", beacon_server="127.0.0.1", beacon_port="31337", report_server="127.0.0.1",
                 report_port="32337", listener_port="32337", input_conf="node_config.xml"):
        self._tree = ET.parse(input_conf)
        self._root = self._tree.getroot()
        self._beacon = self._root.find("beacon")
        self._report = self._root.find("reporting")
        self._listener = self._root.find("listener")
        self._program = self._root.find("program")
        self._fuzzer = self._root.find("fuzzing")
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


class ConfigParser:
    def __init__(self, config):
        self._logger = logging.getLogger(__name__)
        try:
            self._root = ET.fromstring(config)
            self._node_name = self._root.attrib['name']
            self._node_mode = self._root.attrib['mode']
            if self._node_mode == "net":
                beacon = self._root.find("beacon")
                reporting = self._root.find("reporting")
                listener = self._root.find("listener")
                self._beacon_server = beacon.attrib['server']
                self._beacon_port = int(beacon.attrib['port'])
                self._beacon_interval = int(beacon.attrib['interval'])
                self._report_server = reporting.attrib['server']
                self._report_port = reporting.attrib['port']
                self._listener_port = int(listener.attrib['port'])
            elif self._node_mode != "single":
                raise ValueError("Only net and single are available modes for node!")
            self._program_path = self._root.find("program").attrib['path']
            self._program_dbg_child = bool(self._root.find("program").attrib['dbg_child'])
            self._program_sleep_time = int(self._root.find("program").attrib['sleep_time'])
            fuzzer = self._root.find("fuzzer")
            self._fuzzer_type = fuzzer.attrib['type']
            self._fuzz_config = []
            if self._fuzzer_type == "bytemutation":
                self._fuzz_config.append(("Fuzz File", fuzzer.attrib['fuzz_file']))
                self._fuzz_config.append(("Min Change", int(fuzzer.attrib['min_change'])))
                self._fuzz_config.append(("Max Change", int(fuzzer.attrib['max_change'])))
                self._fuzz_config.append(("Seed",int(fuzzer.attrib['seed'])))
            elif self._fuzzer_type == "js_fuzzer":
                self._fuzz_config.append(("Starting Elements", int(fuzzer.attrib['starting_elements'])))
                self._fuzz_config.append(("Total Operations", int(fuzzer.attrib['total_operations'])))
                self._fuzz_config.append(("Browser", fuzzer.attrib['browser']))
                self._fuzz_config.append(("Seed", int(fuzzer.attrib['seed'])))
            else:
                raise ValueError("Unsupported fuzzing type!")
            self._fuzz_config.append(("File Type", fuzzer.attrib['file_type']))
        except Exception as ex:
            self._logger.error("General error occurred while parsing config: " + ex.message + str(ex.args))
            quit()

    @property
    def node_name(self):
        return self._node_name

    @property
    def node_mode(self):
        return self._node_mode

    @property
    def beacon_config(self):
        return self._beacon_server, self._beacon_port, self._beacon_interval if self._node_mode == "net" else None

    @property
    def report_config(self):
        return self._report_server, self._report_port if self._node_mode == "net" else None

    @property
    def listener_config(self):
        return self._listener_port if self._node_mode == "net" else None

    @property
    def program_path(self):
        return self._program_path

    @property
    def dbg_child(self):
        return self._program_dbg_child

    @property
    def sleep_time(self):
        return self._program_sleep_time

    @property
    def fuzzer_type(self):
        return self._fuzzer_type

    @property
    def fuzzer_config(self):
        return self._fuzz_config

    def dump_additional_information(self):
        general_config = [("Program Path", self.program_path), ("Debug Child", str(self.dbg_child)),
                          ("Sleep Time", str(self.sleep_time)), ("Fuzzer Type", self.fuzzer_type)]
        fuzz_conf = [(x[0], str(x[1])) for x in self.fuzzer_config]
        return general_config + fuzz_conf