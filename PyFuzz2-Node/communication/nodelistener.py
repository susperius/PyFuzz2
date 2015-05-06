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
        self._port = port
        self._serving = False
        self._serving_greenlet = None
        self._node_server = None
        self._logger = logging.getLogger(__name__)
        self._task_queue = task_queue

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
        self._logger.debug("Received a job from " + address[0])
        self._task_queue.put(Task(ord(job[0]), address[0], job[1:]))

    def __serve(self):
        self._logger.info("[Listener] initialized on port " + str(self._port) + " ...")
        self._node_server = StreamServer(('', self._port), self.__listener_receiver)
        self._node_server.serve_forever()

    def serve(self):
        if not self._serving:
            self._serving_greenlet = gevent.spawn(self.__serve)
            self._serving = True
            gevent.sleep(0)
        else:
            pass
