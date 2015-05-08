__author__ = 'susperius'

import gevent
import pickle
import logging
import os
from worker import Worker


class ReportWorker(Worker):
    def __init__(self, report_queue, node_dict):
        self._logger = logging.getLogger(__name__)
        self._greenlet = None
        self._report_queue = report_queue
        self._nodes = node_dict

    def __worker_green(self):
        while True:
            if not self._report_queue.empty():
                address, data_packed = self._report_queue.get_nowait()
                data_unpacked = pickle.loads(data_packed)
                report_type = data_unpacked[0]
                if report_type == 0xFF:
                    file_type = data_unpacked[1]
                    program = data_unpacked[2]
                    report = data_unpacked[3]
                    node_name = self._nodes[address].name
                    self.__report_crash_local(node_name, file_type, program, report)
                    self._nodes[address].crashed()
            gevent.sleep(0)

    def start_worker(self):
        if self._greenlet is None:
            self._greenlet = gevent.spawn(self.__worker_green)
            gevent.sleep(0)

    def stop_worker(self):
        if self._greenlet is not None:
            gevent.kill(self._greenlet)

    @staticmethod
    def __parse_string_report(crash, value, end_marker="\r"):
        start = crash.find(value) + len(value)
        end = crash.find(end_marker, start)
        return crash[start:end]

    def __report_crash_local(self, node_name, file_type, program, crash):
        classification = self.__parse_string_report(crash[0], "Exploitability Classification: ")
        description = self.__parse_string_report(crash[0], "Short Description: ")
        hash_val = self.__parse_string_report(crash[0], "(Hash=", ")")
        hash_val = hash_val.split(".")
        directory = "results\\" + node_name + "\\" + classification + "\\" + description + "\\" + hash_val[0] + "\\" + hash_val[1]
        if os.path.exists(directory):
            self._logger.info("duplicated crash")
        else:
            self._logger.info("New unique crash -> \r\n\tclass = " + classification +
                              " \r\n\tShort Description = " + description +
                              " \r\n\tsaved in " + directory)
            os.makedirs(directory)
            with open(directory + "\\crash_report.txt", 'w+') as fd_rep, open(
                                    directory + "\\crash_file." + file_type, "wb+") as fd_crash:
                fd_rep.write(crash[0])
                fd_crash.write(crash[1])
