__author__ = 'susperius'

import logging
from urlparse import parse_qs

import gevent
import gevent.monkey
from gevent.queue import Queue

import node.model.config
from communication.beaconserver import BeaconServer
from communication.reportserver import ReportServer
from communication.webserver import WebServer
from model.config import ConfigParser
from worker.databaseworker import DatabaseWorker
from worker.beaconworker import BeaconWorker
from worker.reportworker import ReportWorker
from worker.nodeclientworker import NodeClientWorker
from web.main import WebSite
from node.model.message_types import MESSAGE_TYPES
gevent.monkey.patch_all()

CONFIG_FILENAME = "server_config.xml"


class PyFuzz2Server:
    def __init__(self, logger, config_filename=CONFIG_FILENAME):
        self._node_dict = {}
        self._crash_dict = {}
        self._logger = logger
        self._config = ConfigParser(config_filename)
        self._beacon_port, self._beacon_timeout = self._config.beacon_config
        self._report_port = self._config.report_server_config
        self._web_port = self._config.web_server_config
        self._beacon_queue = Queue()
        self._node_queue = Queue()
        self._report_queue = Queue()
        self._web_queue = Queue()
        self._db_queue = Queue()
        self._db_worker = DatabaseWorker(self._db_queue, self._node_dict, self._crash_dict)
        self._db_worker.load()
        self._beacon_server = BeaconServer(self._beacon_port, self._beacon_queue)
        self._beacon_worker = BeaconWorker(self._beacon_queue, self._node_queue, self._db_queue,
                                           self._beacon_timeout, self._node_dict)
        self._report_server = ReportServer(self._report_port, self._report_queue)
        self._report_worker = ReportWorker(self._report_queue, self._db_queue, self._node_dict, self._crash_dict)
        self._node_client_worker = NodeClientWorker(self._node_queue)
        self._web_server = WebServer(self._web_port, self._web_queue, self.web_main)

    def main(self):
        self._logger.info("PyFuzz2 Server started...")
        self._beacon_server.serve()
        self._beacon_worker.start_worker()
        self._report_server.serve()
        self._report_worker.start_worker()
        self._web_server.serve()
        self._node_client_worker.start_worker()
        self._db_worker.start_worker()
        while True:
            try:
                gevent.wait()
            except KeyboardInterrupt:
                exit(0)

    def web_main(self, environ, start_response):
        site = WebSite()
        func = "home"
        if environ['PATH_INFO'] == "/index.py" or environ['PATH_INFO'] == "/":
            parameters = parse_qs(environ['QUERY_STRING'])
            if "func" in parameters:
                func = parameters['func'][0] if parameters['func'][0] in site.funcs else "home"
            if func == "home":
                if 'reboot' in parameters:
                    key = parameters['reboot'][0]
                    self._beacon_worker.nodes[key].status = False
                    self._node_queue.put([(key, self._beacon_worker.nodes[key].listener_port), MESSAGE_TYPES['RESET'],
                                          ""])
                if "submit" in parameters and "node" in parameters:
                    key = parameters['node'][0]
                    self._logger.debug("Preparing new config")
                    node_conf = node.model.config.ConfigParser.create_config(environ['wsgi.input'].read())
                    self._beacon_worker.nodes[key].status = False
                    self._node_queue.put([(key, self._beacon_worker.nodes[key].listener_port),
                                         MESSAGE_TYPES['SET_CONFIG'], node_conf])
                if "del" in parameters:
                    key = parameters['del'][0]
                    del(self._beacon_worker.nodes[key])
                status, headers, html = site.home(self._beacon_worker.nodes)
            elif func == "node_detail":
                if "node" in parameters and parameters['node'][0] in self._beacon_worker.nodes.keys():
                    key = parameters['node'][0]
                    status, headers, html = site.node_detail(self._beacon_worker.nodes[key])
                else:
                    status, headers, html = site.file_not_found()
            elif func == "stats":
                status, headers, html = site.stats(self._node_dict, self._crash_dict)
        elif environ['PATH_INFO'] == "/style.css":
            status, headers, html = site.get_style()
        elif environ['PATH_INFO'] == "/scripts.js":
            status, headers, html = site.get_scripts()
        else:
            status, headers, html = site.file_not_found()
        if self._logger.level == logging.DEBUG:
            html += "<br><br>" + str(environ) + "<br><br>" + func + "<br><br>" + environ['wsgi.input'].read()
        start_response(status, headers)
        return [str(html)]


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    server = PyFuzz2Server(logger)
    server.main()
