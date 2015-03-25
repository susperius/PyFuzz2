__author__ = 'susperius'

import logging

import gevent
import gevent.monkey
from gevent.server import DatagramServer

from model.task import Task


'''
THIS CLASS IS NOT MEANT TO BE INSTANTIATED
'''
class BaseServer():
    def __init__(self, port, task_queue):
        self.port = port
        self.serving = False
        self.serving_greenlet = None
        self.beacon_server = None
        self.logger = logging.getLogger(__name__)
        self.task_queue = task_queue

    def __serve(self):
        pass

    def serve(self):
        pass