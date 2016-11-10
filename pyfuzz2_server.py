import logging
import gevent
import gevent.monkey
from gevent.queue import Queue

from communication.beaconserver import BeaconServer
from communication.reportserver import ReportServer
from communication.webserver import WebServer
from worker.databaseworker import DatabaseWorker
from worker.beaconworker import BeaconWorker
from worker.reportworker import ReportWorker
from worker.nodeclientworker import NodeClientWorker
from worker.webworker import WebWorker
from model.config import ConfigParser
from web.app import WebInterface
gevent.monkey.patch_all()

CONFIG_FILENAME = "server_config.xml"


class PyFuzz2Server:
    def __init__(self, logger, config_filename=CONFIG_FILENAME):
        self._node_dict = {}
        self._crash_dict = {}
        self._logger = logger
        self._config = ConfigParser(config_filename)
        beacon_port, beacon_timeout, config_req_interval = self._config.beacon_config
        report_port = self._config.report_server_config
        web_port = self._config.web_server_config
        self._beacon_queue = Queue()
        self._node_queue = Queue()
        self._report_queue = Queue()
        self._web_queue = Queue()
        self._db_queue = Queue()
        self._db_worker = DatabaseWorker(self._db_queue, self._node_dict, self._crash_dict)
        self._db_worker.load()
        self._web_intf = WebInterface(self._web_queue, self._node_dict, self._crash_dict)
        self._web_server = WebServer(web_port, self._web_intf.app)
        self._beacon_server = BeaconServer(beacon_port, self._beacon_queue)
        self._report_server = ReportServer(report_port, self._report_queue)
        self._beacon_worker = BeaconWorker(self._beacon_queue, self._node_queue, self._db_queue,
                                           beacon_timeout, config_req_interval, self._node_dict)
        self._report_worker = ReportWorker(self._report_queue, self._db_queue, self._node_dict, self._crash_dict)
        self._node_client_worker = NodeClientWorker(self._node_queue)
        self._web_worker = WebWorker(self._node_dict, self._web_queue, self._node_queue, self._db_queue)

    def main(self):
        self._logger.info("PyFuzz2 Server started...")
        self._beacon_server.start_server()
        self._beacon_worker.start_worker()
        self._report_server.start_server()
        self._report_worker.start_worker()
        self._web_server.start_server()
        self._node_client_worker.start_worker()
        self._db_worker.start_worker()
        self._web_worker.start_worker()
        while True:
            try:
                gevent.wait()
            except KeyboardInterrupt:
                self.__shut_down()
                exit(0)

    def __shut_down(self):
        self._beacon_server.stop_server()
        self._beacon_worker.stop_worker()
        self._report_server.stop_server()
        self._report_worker.stop_worker()
        self._web_server.stop_server()
        self._node_client_worker.stop_worker()
        self._db_worker.stop_worker()
        self._web_worker.stop_worker()
        gevent.sleep(0)


if __name__ == "__main__":
    #logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    logger = logging.getLogger("PyFuzz2-Server")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("log/server.log")
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    fh.setFormatter(file_formatter)
    ch.setFormatter(console_formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    server = PyFuzz2Server(logger)
    server.main()
