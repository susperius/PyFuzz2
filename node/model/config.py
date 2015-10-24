__author__ = 'susperius'

import xml.etree.ElementTree as ET
import logging
try:
    from node.fuzzing.fuzzers import FUZZERS
except ImportError:
    pass
try:
    from fuzzing.fuzzers import FUZZERS
except ImportError:
    pass
try:
    from node.reducing.reducers import REDUCERS
except ImportError:
    pass
try:
    from reducing.reducers import REDUCERS
except ImportError:
    pass


PROGRAM_ATTRIBUTES = ["path", "dbg_child", "name", "use_http", "sleep_time"]


class ConfigParser:
    def __init__(self, config_filename, from_string=False):
        self._logger = logging.getLogger(__name__)
        self._programs = []
        try:
            if not from_string:
                self._tree = ET.parse(config_filename)
                self._root = self._tree.getroot()
            else:
                self._root = ET.fromstring(config_filename)
            self._node_name = self._root.attrib['name']
            self._node_net_mode = self._root.attrib['net_mode']
            self._node_op_mode = self._root.attrib['op_mode']
            if self._node_net_mode == "net":
                beacon = self._root.find("beacon")
                reporting = self._root.find("reporting")
                listener = self._root.find("listener")
                self._beacon_server = beacon.attrib['server']
                self._beacon_port = int(beacon.attrib['port'])
                self._beacon_interval = int(beacon.attrib['interval'])
                self._report_server = reporting.attrib['server']
                self._report_port = reporting.attrib['port']
                self._listener_port = int(listener.attrib['port'])
            elif self._node_net_mode != "single":
                raise ValueError("Only net and single are available modes for node!")
            programs = self._root.find("programs")
            sleep_times = []
            for prog in programs:
                sleep_times.append(prog.attrib['sleep_time'])
                self._programs.append(prog.attrib)
            # self._program_path = self._root.find("program").attrib['path']
            # self._program_dbg_child = bool(self._root.find("program").attrib['dbg_child'])
            self._sleep_time = max(sleep_times)
            if self._node_op_mode == 'fuzzing':
                fuzzer = self._root.find("fuzzer")
                self._fuzzer_type = fuzzer.attrib['type']
                self._fuzz_config = []
                if self._fuzzer_type not in FUZZERS.keys():
                    raise ValueError("Unsupported fuzzing type")
                for elem in FUZZERS[self._fuzzer_type][0]:
                    self._fuzz_config.append(fuzzer.attrib[elem])
                self._file_type = fuzzer.attrib['file_type']
            elif self._node_op_mode == 'reducing':
                reducer = self._root.find('reducer')
                self._reducer_type = reducer.attrib['type']
                self._reducer_config = []
                if self._reducer_type not in REDUCERS.keys():
                    raise ValueError('Unsupported reducing type')
                for elem in REDUCERS[self._reducer_type]:
                    self._reducer_config.append(reducer.attrib[elem])
                self._file_type = reducer.attrib['file_type']
            else:
                raise ValueError('Unsupported Operation Mode!')
        except Exception as ex:
            self._logger.error("General error occurred while parsing config: " + str(ex.message) + str(ex.args))
            quit()

    @property
    def node_name(self):
        return self._node_name

    @property
    def node_net_mode(self):
        return self._node_net_mode

    @property
    def node_op_mode(self):
        return self._node_op_mode

    @property
    def beacon_config(self):
        return self._beacon_server, self._beacon_port, self._beacon_interval if self._node_net_mode == "net" else None

    @property
    def report_config(self):
        return self._report_server, self._report_port if self._node_net_mode == "net" else None

    @property
    def listener_config(self):
        return self._listener_port if self._node_net_mode == "net" else None

    @property
    def programs(self):
        return self._programs

    @property
    def sleep_time(self):
        return int(self._sleep_time)

    @property
    def file_type(self):
        return self._file_type

    @property
    def fuzzer_type(self):
        return self._fuzzer_type

    @property
    def fuzzer_config(self):
        return self._fuzz_config

    @property
    def reducer_type(self):
        return self._reducer_type

    @property
    def reducer_config(self):
        return self._reducer_config

    def dump_additional_information(self):
        general_config = [("Beacon Server", self._beacon_server),
                          ("Beacon Port", str(self._beacon_port)),
                          ("Beacon Interval", str(self._beacon_interval)),
                          ("Report Server", self._report_server),
                          ("Report Port", str(self._report_port))]
        if self.node_op_mode == 'fuzzing':
            op_mode_conf = {"fuzzer_type": self._fuzzer_type, "fuzz_conf": {}}
            i = 0
            for opt in FUZZERS[self._fuzzer_type][0]:
                op_mode_conf["fuzz_conf"][opt] = self._fuzz_config[i]
                i += 1
        else:
            op_mode_conf = None
        return general_config, self._programs, op_mode_conf

    @staticmethod
    def create_config(data):  # TODO: figure out how to build a new programs list from the submitted data
        in_data = data.replace("+", " ").replace("%5C", "\\").replace("%3A", ":").split("&")
        conf = {}
        programs = {}
        for elem in in_data:
            value = elem.split("=")
            if "prog" not in value[0]:
                conf[value[0].replace(" ", "_")] = value[1]
            else:
                pass
                prog_no, key = value[0].split(" ")
                if prog_no not in programs.keys():
                    programs[prog_no] = {}
                programs[prog_no][key] = value[1]
        conf['programs'] = []
        for key, prog in programs.items():
            pass
            conf['programs'].append(prog)
        node_config = NodeConfig(conf.pop('node_name'), conf.pop('beacon_server'), conf.pop('beacon_port'),
                                 conf.pop('report_server'), conf.pop('report_port'), conf.pop('listener_port'),
                                 "node/node_config.xml")
        node_config.set_beacon_interval(conf.pop('beacon_interval'))
        node_config.set_programs(conf.pop('programs'))
        node_config.set_fuzzer(conf.pop('fuzzer_type'), conf)
        return node_config.dump()


class NodeConfig:
    def __init__(self, node_name="dummyNode", beacon_server="127.0.0.1", beacon_port="31337", report_server="127.0.0.1",
                 report_port="32337", listener_port="32337", input_conf="node_config.xml"):
        self._tree = ET.parse(input_conf)
        self._root = self._tree.getroot()
        self._root.attrib["net_mode"] = "net"
        self._op_mode = self._root.attrib['op_mode']
        self._beacon = self._root.find("beacon")
        self._report = self._root.find("reporting")
        self._listener = self._root.find("listener")
        self._root.remove(self._root.find("programs"))
        self._programs = ET.SubElement(self._root, "programs")
        if self._op_mode == "fuzzing":
            self._fuzzer = self._root.find("fuzzer")
        elif self._op_mode == "reducing":
            self._reducer = self._root.find('reducer')
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

#    def add_program(self, program):
#        self._programs.append(program)

    def set_programs(self, programs):
        for program in programs:
            prog = ET.SubElement(self._programs, "program")
            for key, val in program.items():
                prog.attrib[key] = str(val)

    def set_fuzzer(self, type, arg_dict):
        self._fuzzer.attrib['type'] = type
        for key in arg_dict.keys():
            self._fuzzer.attrib[key] = arg_dict[key]

    def dump(self):
        return ET.tostring(self._root)
