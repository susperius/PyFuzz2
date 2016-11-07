import logging


class Server:
    def __init__(self):
        self._logger = logging.getLogger("PyFuzz2-Server")

    def start_server(self):
        raise NotImplementedError("ABSTRACT METHOD")

    def stop_server(self):
        raise NotImplementedError("ABSTRACT METHOD")