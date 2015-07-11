__author__ = 'susperius'

import gevent
import logging
import pickle
from gevent.queue import Queue
from model.message_types import MESSAGE_TYPES
from worker import Worker


class ListenerWorker(Worker):
    def __init__(self, listener_queue, report_queue):
        self._logger = logging.getLogger(__name__)
        self._listener_queue = listener_queue
        self._report_queue = report_queue
        self._new_config = False
        self._running = False
        self._reset = False
        self._greenlet = None

    def __worker_green(self):
        while self._running:
            if not self._listener_queue.empty():
                actual_task = self._listener_queue.get_nowait()
                self._listener_worker(actual_task)
            gevent.sleep(0)

    def _listener_worker(self, task):
        msg_type, msg = pickle.loads(task[1])
        self._logger.debug("Listener Worker -> Type:" + str(msg_type))
        if msg_type in MESSAGE_TYPES.keys():
            if msg_type == 0x01:
                pass
            elif msg_type == 0x02:  # SET_CONFIG
                self._set_config(msg)
            elif msg_type == 0x03:  # GET_CONFIG
                self._report_queue.put([0x03, ""])
            elif msg_type == 0x04:
                pass
            elif msg_type == 0x05:  # RESET
                self._reset = True
            elif msg_type == 0x06:
                pass
            elif msg_type == 0xFF:
                pass

    def _set_config(self, msg):
        with open("node_config.xml", 'w+') as fd:
            fd.write(msg)
        # trigger reload the config
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
            self._running = True
            self._greenlet = gevent.spawn(self.__worker_green)
            gevent.sleep(0)

    def stop_worker(self):
        if self._running:
            self._running = False
            gevent.kill(self._greenlet)

