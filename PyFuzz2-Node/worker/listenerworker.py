__author__ = 'susperius'

import gevent
import logging

from gevent.queue import Queue
from model.task import Task
from model.message_types import MESSAGE_TYPES
from worker import Worker


class ListenerWorker(Worker):
    def __init__(self, listener_queue):
        self._logger = logging.getLogger(__name__)
        self._listener_queue = listener_queue
        self._new_config = False
        self._running = False
        self._reset = False
        self._greenlet = None

    def __worker_green(self):
        while True:
            if not self._listener_queue.empty():
                actual_task = self._listener_queue.get_nowait()
                self._listener_worker(actual_task.get_task())
            gevent.sleep(0)

    def _listener_worker(self, task):
        self._logger.debug("Listener Worker -> Type:" + str(task['type']) + "| " + task['msg'])
        if task['type'] in MESSAGE_TYPES.keys():
            if task['type'] == 0x01:
                pass
            elif task['type'] == 0x02:
                pass
            elif task['type'] == 0x03:  # SET_CONFIG
                self._set_config(task['msg'])
            elif task['type'] == 0x04:  # GET_CONFIG
                pass
            elif task['type'] == 0x05:  # RESET
                self._reset = True
            elif task['type'] == 0x06:
                pass
            elif task['type'] == 0xFF:
                pass

    def _set_config(self, msg):
        with open("node_config.xml", 'w+') as fd:
            fd.write(msg)
        #trigger reload the config
        self._new_config = True
        pass

    @property
    def new_config(self):
        if self._new_config:
            self._new_config = False
            return True
        else:
            return False

    @property
    def reset(self):
        return self._reset

    def start_worker(self):
        if not self._running:
            self._greenlet = gevent.spawn(self.__worker_green)
            self._running = True
            gevent.sleep(0)

    def stop_worker(self):
        gevent.kill(self._greenlet)
        self._running = False
