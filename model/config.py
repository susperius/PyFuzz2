__author__ = 'susperius'

import xml.etree.ElementTree as ET
import logging


class ConfigParser:
    def __init__(self, config_filename):
        self._logger = logging.getLogger(__name__)
        try:
            self._tree = ET.parse(config_filename)
            self._root = self._tree.getroot()
            beacon = self._root.find("beacon")
            web_server = self._root.find("web_server")
            report_server = self._root.find("report_server")
            self._beacon_port = int(beacon.attrib['port'])
            self._beacon_timeout = int(beacon.attrib['timeout'])
            self._config_req_interval = int(beacon.attrib['config_req_interval'])
            self._web_port = int(web_server.attrib['port'])
            self._report_port = int(report_server.attrib['port'])

        except Exception as ex:
            self._logger.error("General error occurred while parsing config: " + ex.message)
            quit()

    @property
    def beacon_config(self):
        return self._beacon_port, self._beacon_timeout, self._config_req_interval

    @property
    def web_server_config(self):
        return self._web_port

    @property
    def report_server_config(self):
        return self._report_port
