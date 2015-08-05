__author__ = 'susperius'

import gevent
import pickle
import logging
import os
from communication.reportclient import ReportClient
from worker import Worker
from model.message_types import MESSAGE_TYPES
from utils.html_css_splitter import is_two_files, split_files


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
            msg_type, msg = self._report_queue.get()
            self._logger.debug("Report job Type --> " + str(msg_type))
            if MESSAGE_TYPES['CRASH'] == msg_type:
                self.__report_crash_local(msg)
                if self._net_mode:
                    data_string = pickle.dumps([msg_type, self._file_type, self._program, msg], -1)
                    self._client.send(data_string)
            elif MESSAGE_TYPES['GET_CONFIG'] == msg_type:
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
    def parse_string_report(crash, value, end_marker="\r"):
        start = crash.find(value) + len(value)
        end = crash.find(end_marker, start)
        if end_marker == "\r" and end == -1:
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
            if is_two_files(crash[1]):
                files = split_files(crash[1], "crash_file." + self._file_type)
                with open(directory + "/" + files.keys()[0], 'wb+') as file1_fd, open(directory + "/" + files.keys()[1], 'wb+') as file2_fd:
                    file1_fd.write(files[files.keys()[0]])
                    file2_fd.write(files[files.keys()[1]])
            else:
                with open(directory + "/crash_file." + self._file_type, "wb+") as fd_crash:
                    fd_crash.write(crash[1])
            with open(directory + "/crash_report.txt", 'w+') as fd_rep:
                fd_rep.write(crash[0])