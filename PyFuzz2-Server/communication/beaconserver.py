__author__ = 'susperius'

import logging

import gevent
import gevent.monkey
from gevent.server import DatagramServer

from model.task import Task
from baseserver import BaseServer


gevent.monkey.patch_all()


class BeaconServer(BaseServer):
    def __init__(self, port, task_queue):
        BaseServer.__init__(self, port, task_queue)

    def __serve(self):
        self.logger.info("[Beacon Server] initialized on port " + str(self.port) + " ...")
        self.beacon_server = DatagramServer(('', self.port), self.__beacon_receiver)
        self.beacon_server.serve_forever()

    def __beacon_receiver(self, msg, address):
        if ord(msg[0]) == 0x01:
            self.task_queue.put(Task(0x01, address[0], msg[1:]))

    def serve(self):
        if not self.serving:
            self.serving_greenlet = gevent.spawn(self.__serve)
            self.serving = True
            gevent.sleep(0)
        else:
            pass
