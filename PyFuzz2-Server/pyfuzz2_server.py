__author__ = 'susperius'

import logging
import gevent
import gevent.monkey

from model.task import Task
from model.message_types import MESSAGE_TYPES
from gevent.queue import Queue
from communication.beaconserver import BeaconServer

gevent.monkey.patch_all()


def main():
    logger.info("PyFuzz2 Server started...")
    task_queue = Queue()
    beacon_server = BeaconServer(31337, task_queue)
    beacon_server.serve()
    while True:
        try:
            if not task_queue.empty():
                actual_task = task_queue.get_nowait()
                task_worker(actual_task)
                pass
            gevent.sleep(0)
            pass
        except KeyboardInterrupt:
            exit(0)


def task_worker(task):
    logger.debug("Task_Worker called: " + MESSAGE_TYPES[task.get_task()['type']] + ": From: " + task.get_task()['sender'] + " with Message: " + task.get_task()['msg'])


if __name__=="__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    main()