__author__ = 'susperius'

import gevent
import gevent.socket
import os


class ReportClient:
    def __init__(self, report_server, report_server_port):
        self._server = report_server
        self._port = report_server_port

    def send(self, data):
        try:
            sock = gevent.socket.create_connection((self._server, self._port))
            sock.send(data)
            sock.close()
        except IOError:
            pass  # TODO: think about a more reliable solution ... this is just to be sure the reportworker isn't
                  # is not crashing and to keep the node working ....