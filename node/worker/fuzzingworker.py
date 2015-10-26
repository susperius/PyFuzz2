__author__ = 'susperius'

import gevent
import os
import time
import psutil
import subprocess
import logging
from debugging.windbg import Debugger
from worker import Worker


class FuzzingWorker(Worker):
    def __init__(self, programs, fuzzer, report_queue):
        self._logger = logging.getLogger(__name__)
        self._greenlet = None
        self._process = None
        self._web_process = None
        self._running = False
        self._programs = programs
        self._need_web_server = False
        for prog in programs:
            if bool(prog['use_http']):
                self._need_web_server = True
        self._testcase = ""
        self._crash_report = ""
        self._fuzzer = fuzzer
        self._report_queue = report_queue
        self._DEVNULL = os.open(os.devnull, os.O_RDWR)

    def __worker_green(self):
        count = 0
        while self._running:
            self._logger.info("Creating Testcases...\r\n\tnumber: " + str(count) + " to " + str(count + 100))
            self.__create_testcases()
            self._logger.info("Start testing...")
            dir_listing = os.listdir("testcases/")
            if self._need_web_server:
                self._web_process = subprocess.Popen("python -m SimpleHTTPServer 8080", stdout=self._DEVNULL,
                                                     stderr=self._DEVNULL, cwd="testcases/")
            for filename in dir_listing:
                if self._fuzzer.file_type not in filename:
                        continue
                count += 1
                for prog in self._programs:
                    if not self._running:
                        break
                    testcase_dir = os.getcwd() + "\\testcases\\"
                    if bool(prog['dbg_child']):
                        if bool(prog['use_http']):
                            self._process = subprocess.Popen(
                                "python debugging\\windbg.py -p \"" + prog['path']
                                + "\" -t \"http://127.0.0.1:8080/" + filename + "\" -c True",
                                stdout=subprocess.PIPE)
                        else:
                            self._process = subprocess.Popen(
                                "python debugging\\windbg.py -p \"" + prog['path']
                                + "\" -t \"" + testcase_dir + filename + "\" -c True",
                                stdout=subprocess.PIPE)
                    else:
                        if bool(prog['use_http']):
                            self._process = subprocess.Popen(
                                "python debugging\\windbg.py -p \"" + prog['path']
                                + "\" -t \"http://127.0.0.1:8080/" + filename + "\"",
                                stdout=subprocess.PIPE)
                        else:
                            self._process = subprocess.Popen(
                                "python debugging\\windbg.py -p \"" + prog['path']
                                + "\" -t \"" + testcase_dir + filename + "\"",
                                stdout=subprocess.PIPE)
                    self._logger.debug("Debugger started...\r\n\tprogram: " + prog['name'] + " testcase: " + filename +
                                       " #testcases: " + str(count))
                    gevent.sleep(int(prog['sleep_time']))
                    self._process.kill()
                    if os.path.isfile("tmp_crash_report"):
                        with open("tmp_crash_report") as fd:
                            crash_report = fd.read()
                        os.remove("tmp_crash_report")
                        testcases = []
                        with open(testcase_dir + filename, "rb") as fd:
                            testcases.append((filename, fd.read()))
                        test_file = filename.split(".")
                        for single_file in dir_listing:
                            if single_file.startswith(test_file[0]) and test_file[1] not in single_file:
                                with open(testcase_dir + single_file, "rb") as add_fd:
                                    testcases.append((single_file, add_fd.read()))
                        # Structure crash message (0xFF, (prog['name'], crash_report, testcases[]))
                        self._report_queue.put((0xFF, (prog['name'], crash_report, testcases)))
                    gevent.sleep(1)
            if self._need_web_server:
                self._web_process.kill()

    def __create_testcases(self):
        self._fuzzer.create_testcases(100, "testcases")

    def start_worker(self):
        if self._greenlet is None:
            self._running = True
            self._greenlet = gevent.spawn(self.__worker_green)

    def stop_worker(self):
        if self._greenlet is not None:
            self._running = False
            gevent.kill(self._greenlet)
            try:
                self._process.kill()
                self._process.terminate()
                os.close(self._DEVNULL)
            except Exception as ex:
                self._logger.debug("Exception occured while killing Debugger: " + ex.message)

