__author__ = 'susperius'

import gevent
import pickle
import logging
import os
from communication.reportclient import ReportClient
from worker import Worker


class ReportWorker(Worker):
    def __init__(self, net_mode, report_queue, file_type, program, report_server="", report_server_port=0):
        self._logger = logging.getLogger(__name__)
        self._report_queue = report_queue
        self._net_mode = net_mode
        self._greenlet = None
        self._file_type = file_type
        self._program = program
        if self._net_mode:
            self._client = ReportClient(report_server, report_server_port)
        self._running = False

    def __worker_green(self):
        while self._running:
            if not self._report_queue.empty():
                msg_type, msg = self._report_queue.get_nowait()
                if msg_type == 0xFF:
                    self.__report_crash_local(msg)
                    if self._net_mode:
                        data_string = pickle.dumps([msg_type, self._file_type, self._program, msg], -1)
                        self._client.send(data_string)
                elif msg_type == 0x03:
                    with open("node_config.xml", 'r') as fd:
                        config = fd.read()
                    self._client.send(pickle.dumps([msg_type, config], -1))
            gevent.sleep(0)

    def start_worker(self):
        if self._greenlet is None:
            self._running = True
            self._greenlet = gevent.spawn(self.__worker_green)
            gevent.sleep(0)

    def stop_worker(self):
        if self._greenlet is not None:
            gevent.kill(self._greenlet)

    @staticmethod
    def __parse_string_report(crash, value, end_marker="\r"):
        start = crash.find(value) + len(value)
        end = crash.find(end_marker, start)
        if end_marker=="\r" and end == -1:
            end = crash.find("\n", start)
        return crash[start:end]

    def __report_crash_local(self, crash):
        description = self.parse_string_report(crash[0], "Short Description: ")
        hash_val = self.parse_string_report(crash[0], "(Hash=", ")")
        hash_val = hash_val.split(".")
        directory = "results\\" + description + "\\" + hash_val[0] + "\\" + hash_val[1]
        if os.path.exists(directory):
            self._logger.info("duplicated crash")
        else:
            self._logger.info("New unique crash -> \r\n" +
                              " \r\n\tShort Description = " + description +
                              " \r\n\tsaved in " + directory)
            os.makedirs(directory)
            with open(directory + "\\crash_report.txt", 'w+') as fd_rep, open(
                                    directory + "\\crash_file." + self._file_type, "wb+") as fd_crash:
                fd_rep.write(crash[0])
                fd_crash.write(crash[1])
