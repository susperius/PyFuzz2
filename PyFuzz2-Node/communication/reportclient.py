__author__ = 'susperius'

import gevent
import os

class ReportClient:
    def __init__(self, report_server, report_server_port):
        self._server = report_server
        self._port = report_server_port

    def send(self, data):
        answer = ""
        sock = gevent.socket.create_connection((self._server, self._port))
        sock.send(data)
        fp = sock.makefile()
        while True:
            line = fp.readline()
            if line:
                answer += line
                fp.flush()
            else:
                break
        sock.close()
        return answer
