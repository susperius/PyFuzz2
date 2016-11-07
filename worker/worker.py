import logging


class Worker:
    def __init__(self):
        self._logger = logging.getLogger("PyFuzz2-Server")

    def start_worker(self):
        raise NotImplementedError("ABSTRACT METHOD")

    def stop_worker(self):
       raise NotImplementedError("ABSTRACT METHOD")