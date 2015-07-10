__author__ = 'susperius'

import logging
import gevent
from gevent import pywsgi


class WebServer:
    def __init__(self, port, task_queue, web_main_function):
        self._port = port
        self._serving = False
        self._serving_greenlet = None
        self._web_server = None
        self._logger = logging.getLogger(__name__)
        self._task_queue = task_queue
        self._web_main_function = web_main_function

    def __serve(self):
        self._logger.info("[WebServer] initialized on port " + str(self._port) + " ...")
        self._web_server = pywsgi.WSGIServer(('', self._port), self._web_main_function)
        self._web_server.serve_forever()

    def serve(self):
        if not self._serving:
            self._serving_greenlet = gevent.spawn(self.__serve)
            self._serving = True
            gevent.sleep(0)
        else:
            pass



