__author__ = 'susperius'


import logging

import gevent
import gevent.monkey
import gevent.socket as socket
from gevent.server import StreamServer

from model.task import Task

gevent.monkey.patch_all()

class ReportServer:
    def __init__(self, port, task_queue):
        self.port = port
        self.serving = False
        self.serving_greenlet = None
        self.beacon_server = None
        self.logger = logging.getLogger(__name__)
        self.task_queue = task_queue

    def __report_receiver(self, sock, address):
        fp = sock.makefile()
        while True:
            line = fp.readline()
            if line:
                fp.write(line)
                fp.flush()
            else:
                break
        sock.shutdown(socket.SHUT_WR)
        sock.close()

    def __serve(self):
        self.logger.info("[Report Server] initialized on port " + str(self.port) + " ...")
        self.beacon_server = StreamServer(('', self.port), self.__report_receiver)
        self.beacon_server.serve_forever()

    def serve(self):
        if not self.serving:
            self.serving_greenlet = gevent.spawn(self.__serve)
            self.serving = True
            gevent.sleep(0)
        else:
            pass
