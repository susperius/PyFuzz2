import logging
import gevent
from model.web import WEB_QUEUE_TASKS
from worker import Worker


class WebWorker(Worker):
    '''This class just distributes the jobs from the web app to the other workers'''
    def __init__(self, node_dict, web_queue, node_queue, db_queue):
        self._logger = logging.getLogger(__name__)
        self._node_dict = node_dict
        self._web_queue = web_queue
        self._node_queue = node_queue
        self._db_queue = db_queue
        self._greenlet = None
        self._active = False

    def start_worker(self):
        if not self._active:
            self._greenlet = gevent.spawn(self.__worker_green)
            self._active = True

    def __worker_green(self):
        while self._active:
            job = self._web_queue.get()  # job layout: (WEB_QUEUE_TASK, JOB_SPECIFIC)
            if job[0] == WEB_QUEUE_TASKS['TO_NODE']:
                self._node_queue.put(job[1])
            elif job[0] == WEB_QUEUE_TASKS['TO_DB']:
                self._db_queue.put(job[1])
            gevent.sleep(0)

    def stop_worker(self):
        if self._active:
            gevent.kill(self._greenlet)
            self._active = False
