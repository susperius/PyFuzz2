__author__ = 'susperius'

import xml.etree.ElementTree as ET
import logging


class ConfigParser:
    def __init__(self, config_filename):
        self._logger = logging.getLogger(__name__)
        try:
            self._tree = ET.parse(config_filename)
            self._root = self._tree.getroot()
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
                self._fuzz_config.append(fuzzer.attrib['fuzz_file'])
                self._fuzz_config.append(int(fuzzer.attrib['min_change']))
                self._fuzz_config.append(int(fuzzer.attrib['max_change']))
                self._fuzz_config.append(int(fuzzer.attrib['seed']))
            elif self._fuzzer_type == "js_fuzzer":
                self._fuzz_config.append(int(fuzzer.attrib['starting_elements']))
                self._fuzz_config.append(int(fuzzer.attrib['total_operations']))
                self._fuzz_config.append(fuzzer.attrib['browser'])
                self._fuzz_config.append(int(fuzzer.attrib['seed']))
            else:
                raise ValueError("Unsupported fuzzer type!")
            self._fuzz_config.append(fuzzer.attrib['file_type'])
        except Exception as ex:
            self._logger.error("General error occurred while parsing config: " + ex.message)
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