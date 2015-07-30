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
    def __init__(self, program_path, fuzzer, report_queue, sleep_time, dbg_child=False):
        self._logger = logging.getLogger(__name__)
        self._greenlet = None
        self._process = None
        self._running = False
        self._program_path = program_path
        self._testcase = ""
        self._crash_occurred = False
        self._crash_report = ""
        self._fuzzer = fuzzer
        self._report_queue = report_queue
        self._sleep_time = sleep_time
        self._dbg_child = dbg_child
        self._running = False

    def __worker_green(self):
        #if self._fuzzer.NAME == "js_dom_fuzzer":
        #    web_cwd = os.getcwd() + "/testcases/"
        #    web_process = subprocess.Popen("python -m SimpleHTTPServer 8080", cwd=web_cwd, stdout=subprocess.PIPE,
        #                                   stderr=subprocess.PIPE)
        while self._running:
            self._logger.info("Creating Testcases ...")
            self.__create_testcases()
            self._logger.info("Start testing ...")
            dir_listing = os.listdir("testcases/")
            for filename in dir_listing:
                if not self._running:
                    break
                if self._fuzzer.file_type not in filename:
                    continue
                output = ""
                testcase_dir = os.getcwd() + "\\testcases\\"
                if self._dbg_child:
                    if self._fuzzer.NAME == "js_dom_fuzzer":
                        self._process = subprocess.Popen(
                            "python debugging\\windbg.py -p \"" + self._program_path
                            + "\" -t \"http://127.0.0.1:8080/" + filename + "\" -c True",
                            stdout=subprocess.PIPE)
                    else:
                        self._process = subprocess.Popen(
                            "python debugging\\windbg.py -p \"" + self._program_path
                            + "\" -t \"" + testcase_dir + filename + "\" -c True",
                            stdout=subprocess.PIPE)
                else:
                    if self._fuzzer.NAME == "js_dom_fuzzer":
                        self._process = subprocess.Popen(
                            "python debugging\\windbg.py -p \"" + self._program_path
                            + "\" -t \"http://127.0.0.1:8080/" + filename + "\"",
                            stdout=subprocess.PIPE)
                    else:
                        self._process = subprocess.Popen(
                            "python debugging\\windbg.py -p \"" + self._program_path
                            + "\" -t \"" + testcase_dir + filename + "\"",
                            stdout=subprocess.PIPE)
                self._logger.debug("Debugger started...")
                gevent.sleep(self._sleep_time)
                self._process.kill()
                if os.path.isfile("tmp_crash_report"):
                    with open("tmp_crash_report") as fd:
                        output = fd.read()
                    os.remove("tmp_crash_report")
                    with open(testcase_dir + filename, "rb") as fd:
                        testcase = fd.read()
                    test_file = filename.split(".")
                    for single_file in dir_listing:
                        if single_file.startswith(test_file[0]) and test_file[1] not in single_file:
                            with open(testcase_dir + single_file, "rb") as add_fd:
                                testcase += "-" * 50 + "\r\n\r\nNEW FILE:" + single_file + "\r\n\r\n" + "-" * 50 + "\r\n"
                                testcase += add_fd.read()
                    self._report_queue.put((0xFF, (output, testcase)))
                gevent.sleep(1)

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
            except Exception as ex:
                self._logger.debug("Exception occured while killing Debugger: " + ex.message)

