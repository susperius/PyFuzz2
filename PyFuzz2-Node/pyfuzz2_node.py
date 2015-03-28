__author__ = 'susperius'

import logging
import gevent
import gevent.monkey

from communication.beaconclient import BeaconClient
from communication.tcplistener import Listener
from gevent.queue import Queue

gevent.monkey.patch_all()

def main():
    logger.info("PyFuzz 2 Node started ...")
    task_queue = Queue()
    beacon_client = BeaconClient("127.0.0.1", 31337, "NODE01")
    beacon_client.start_beacon()
    tcp_listener = Listener(32337, task_queue)
    tcp_listener.serve()
    while True:
        try:
            if not task_queue.empty():
                task = task_queue.get_nowait()
                logger.debug(task)
            gevent.sleep(0)
        except KeyboardInterrupt:
            quit()
    pass


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    main()