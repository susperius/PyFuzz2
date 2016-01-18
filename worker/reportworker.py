import gevent
import pickle
import logging
import os
from worker import Worker
from databaseworker import DB_TYPES, SEPARATOR
from node.model.message_types import MESSAGE_TYPES
from model.crash import Crash
from hashlib import md5

__author__ = 'susperius'


class ReportWorker(Worker):
    def __init__(self, report_queue, db_queue, node_dict, crash_dict=None):
        self._logger = logging.getLogger(__name__)
        self._greenlet = None
        self._report_queue = report_queue
        self._db_queue = db_queue
        self._nodes = node_dict
        self._crashes = {} if crash_dict is None else crash_dict

    def __worker_green(self):
        while True:
            address, data_packed = self._report_queue.get()
            data_unpacked = pickle.loads(data_packed)
            msg_type = data_unpacked[0]
            msg = data_unpacked[1]
            if MESSAGE_TYPES['CRASH'] == msg_type:
                # Structure crash message (0xFF, (prog['name'], crash_report, testcases[]))
                self.__report_crash_local(address, msg)
            elif MESSAGE_TYPES['GET_CONFIG'] == msg_type:
                config = msg
                self._nodes[address].config = config
            elif MESSAGE_TYPES['UNKNOWN'] == msg_type:
                # Structure unknown crash message (0xFE, (prog['name'], testcases))
                self.__report_unknown(msg)
            gevent.sleep(0)
            gevent.sleep(1)

    def start_worker(self):
        if self._greenlet is None:
            self._greenlet = gevent.spawn(self.__worker_green)
            gevent.sleep(0)

    def stop_worker(self):
        if self._greenlet is not None:
            gevent.kill(self._greenlet)

    @property
    def crashes(self):
        return self._crashes

    @staticmethod
    def __parse_string_report(crash, value, end_marker="\r\n"):
        start = crash.find(value) + len(value)
        end = crash.find(end_marker, start)
        if end_marker == "\r\n" and end == -1:
            end = crash.find("\n", start)
        return crash[start:end]

    def __report_crash_local(self, node_address, msg):
        prog_name, crash_report, testcases = msg
        classification = self.__parse_string_report(crash_report, "Exploitability Classification: ")
        description = self.__parse_string_report(crash_report, "Short Description: ")
        hash_val = self.__parse_string_report(crash_report, "(Hash=", ")")
        hash_val = hash_val.split(".")
        self._nodes[node_address].crashed(hash_val[0])
        crash_key = prog_name + SEPARATOR + hash_val[0]
        if crash_key not in self._crashes.keys():
            self._crashes[crash_key] = Crash(node_address, prog_name, hash_val[0], hash_val[1],
                                             description, classification)
        else:
            self._crashes[crash_key].add_node_address(node_address)
        self._db_queue.put((DB_TYPES['CRASH'], crash_key))
        directory = "results/" + prog_name + "/" + description + "/" + hash_val[0] + "/" + hash_val[1]
        if os.path.exists(directory):
            self._logger.info("duplicated crash")
        else:
            self._logger.info("New unique crash in " + prog_name + "-> \r\n\tclass = " + classification +
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
