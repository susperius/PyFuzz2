__author__ = 'susperius'

import gevent
import os
import time
import psutil
import subprocess
import logging
from debugging.windbg import Debugger
from worker import Worker


class DebuggerWorker(Worker):
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

    def __worker_green(self):
        while True:
            self._logger.info("Creating Testcases ...")
            self.__create_testcases()
            self._logger("Start testing ...")
            for filename in os.listdir("testcases/"):
                output = ""
                testcase_dir = os.getcwd() + "\\testcases\\"
                if self._dbg_child:
                    self._process = subprocess.Popen(
                        "python debugging\\windbg.py -p \"" + self._program_path
                        + "\" -t \"" + testcase_dir + filename + "\"",
                        stdout=subprocess.PIPE)
                else:
                    self._process = subprocess.Popen(
                        "python debugging\\windbg.py -p \"" + self._program_path
                        + "\" -t \"" + testcase_dir + filename + "\" -c",
                        stdout=subprocess.PIPE)
                self._logger.debug("Debugger started...")
                gevent.sleep(1)
                proc_childs = psutil.Process(self._process.pid).children()
                for child in proc_childs:
                    if child.exe() in self._program_path:
                        if self._dbg_child:
                            proc = child.get_children()[0]
                        else:
                            proc = child
                        break
                start = time.time()
                try:
                    proc.cpu_percent()
                    while True:
                        if time.time() - start > self._sleep_time:
                            break
                        elif proc.cpu_percent(1.0) == 0.0:
                            break
                except:
                    pass # just ignore
                self._process.kill()
                output = self._process.stdout.read()
                if "Crash Report" in output:
                    with open(testcase_dir + filename, "rb") as fd:
                        testcase = fd.read()
                    self._report_queue.put((0xFF, (output, testcase)))
                gevent.sleep(1)

    def __create_testcases(self):
        for i in range(100):
            filename = "test" + str(i) if i > 9 else "test0" + str(i)
            filename += "." + self._fuzzer.file_type
            with open("testcases/" + filename, "wb+") as fd:
                fd.write(self._fuzzer.fuzz())

    def start_worker(self):
        if self._greenlet is None:
            self._greenlet = gevent.spawn(self.__worker_green)

    def stop_worker(self):
        if self._greenlet is not None:
            gevent.kill(self._greenlet)
            try:
                self._process.kill()
                self._process.terminate()
            except Exception as ex:
                self._logger.debug("Exception occured while killing Debugger: " + ex.message)

