import gevent
import pickle
import logging
import os
from hashlib import md5
from communication.reportclient import ReportClient
from worker import Worker
from model.message_types import MESSAGE_TYPES


__author__ = 'susperius'


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
                # Structure crash message (0xFF, (prog['name'], crash_report, testcases[]))
                self.__report_crash_local(msg)
                if self._net_mode:
                    data = pickle.dumps((msg_type, msg), -1)
                    self._client.send(data)
            elif MESSAGE_TYPES['GET_CONFIG'] == msg_type:
                with open("node_config.xml", 'r') as fd:
                    config = fd.read()
                self._client.send(pickle.dumps([msg_type, config], -1))
            elif MESSAGE_TYPES['UNKNOWN'] == msg_type:
                # Structure unknown crash message (0xFE, (prog['name'], testcases))
                self.__report_unknown(msg)
                if self._net_mode:
                    data = pickle.dumps((msg_type, msg), -1)
                    self._client.send(data)
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
    def parse_string_report(crash, value, end_marker="\r\n"):
        start = crash.find(value) + len(value)
        end = crash.find(end_marker, start)
        if end_marker == "\r\n" and end == -1:
            end = crash.find("\n", start)
        return crash[start:end]

    def __report_crash_local(self, msg):
        prog_name, crash_report, testcases = msg
        description = self.parse_string_report(crash_report, "Short Description: ")
        hash_val = self.parse_string_report(crash_report, "(Hash=", ")")
        hash_val = hash_val.split(".")
        directory = "results/" + prog_name + "/" + description + "/" + hash_val[0] + "/" + hash_val[1]
        if os.path.exists(directory):
            self._logger.info("duplicated crash")
        else:
            self._logger.info("New unique crash -> \r\n" +
                              " \r\n\tShort Description = " + description +
                              " \r\n\tsaved in " + directory)
            os.makedirs(directory)
            for testcase in testcases:
                with open(directory + "/" + testcase[0], 'wb+') as fd_case:
                    fd_case.write(testcase[1])
            with open(directory + "/crash_report.txt", 'wb+') as fd_rep:
                fd_rep.write(crash_report)

    @staticmethod
    def __report_unknown(msg):
        prog_name, testcases = msg
        md5_hash = md5()
        md5_hash.update(testcases[0][1])
        directory = "results/" + prog_name + "/" + md5_hash.hexdigest() + "/"
        for testcase in testcases:
            with open(directory + testcase[0], 'wb+') as fd:
                fd.write(testcase[1])
