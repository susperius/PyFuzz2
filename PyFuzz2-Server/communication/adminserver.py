__author__ = 'susperius'

import logging

import gevent
import gevent.monkey
from gevent.server import StreamServer

from model.task import Task
from baseserver import BaseServer

gevent.monkey.patch_all()

class AdminServer(BaseServer):
    def __init__(self, port, task_queue):
        BaseServer.__init__(self, port, task_queue)

    def __serve(self):
        pass

    def __admin_receiver(self, sock, address):
        pass

    def serve(self):
        if not self.serving:
            self.serving_greenlet = gevent.spawn(self.__serve)
            self.serving = True
            gevent.sleep(0)
        else:
            pass

