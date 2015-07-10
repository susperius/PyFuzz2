__author__ = 'susperius'

import gevent
import logging


class Worker:

    def __worker_green(self):
        raise NotImplementedError("ABSTRACT METHOD")

    def start_worker(self):
        raise NotImplementedError("ABSTRACT METHOD")

    def stop_worker(self):
       raise NotImplementedError("ABSTRACT METHOD")