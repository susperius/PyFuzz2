import logging
import gevent
import gevent.monkey
from gevent.server import DatagramServer
from server import Server
gevent.monkey.patch_all()


class BeaconServer(Server):
    def __init__(self, port, task_queue):
        self._port = port
        self._serving = False
        self._serving_greenlet = None
        self._beacon_server = None
        self._logger = logging.getLogger(__name__)
        self._task_queue = task_queue

    def __serve(self):
        self._logger.info("[BeaconServer] initialized on port " + str(self._port) + " ...")
        self._beacon_server = DatagramServer(('', self._port), self.__beacon_receiver)
        self._beacon_server.serve_forever()

    def __beacon_receiver(self, msg, address):
        ipv4_addr, port = address if "ffff" not in address[0] else address[0][7:], address[1]
        self._task_queue.put([(ipv4_addr, port), msg])

    def start_server(self):
        if not self._serving:
            self._serving_greenlet = gevent.spawn(self.__serve)
            self._serving = True
            gevent.sleep(0)

    def stop_server(self):
        if self._serving:
            gevent.kill(self._serving_greenlet)
            self._serving = False
            self._beacon_server.close()
            self._logger.info("[BeaconServer] shut down")
