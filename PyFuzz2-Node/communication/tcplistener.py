__author__ = 'susperius'


import logging

import gevent
import gevent.monkey
import gevent.socket as socket
from gevent.server import StreamServer

from model.task import Task

#gevent.monkey.patch_all()


class Listener:
    def __init__(self, port, task_queue):
        self.port = port
        self.serving = False
        self.serving_greenlet = None
        self.beacon_server = None
        self.logger = logging.getLogger(__name__)
        self.task_queue = task_queue

    def __listener_receiver(self, sock, address):
        job = ""
        fp = sock.makefile()
        while True:
            line = fp.readline()
            if line:
                job += line
                fp.flush()
            else:
                break
        fp.write("RECV\r\n\r\n")
        sock.shutdown(socket.SHUT_WR)
        sock.close()
        self.logger.debug(job)
        self.task_queue.put(Task(ord(job[0]), address[0], job[1:]))

    def __serve(self):
        self.logger.info("[Listener] initialized on port " + str(self.port) + " ...")
        self.beacon_server = StreamServer(('', self.port), self.__listener_receiver)
        self.beacon_server.serve_forever()

    def serve(self):
        if not self.serving:
            self.serving_greenlet = gevent.spawn(self.__serve)
            self.serving = True
            gevent.sleep(0)
        else:
            pass
