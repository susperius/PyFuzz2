__author__ = 'susperius'

import gevent
import os
import time
import psutil
import subprocess
import logging
from debugging.windbg import Debugger


class DebuggerWorker:
    def __init__(self, program_path, fuzzer, report_queue, sleep_time):
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

    def _create_crash_report(self):
        self._crash_report += "Crash Report\r\n"
        self._crash_report += self._dbg.issue_dbg_command(u"r")
        self._crash_report += "\r\n"
        self._crash_report += self._dbg.issue_dbg_command(u"k")
        self._crash_report += "\r\n"
        self._crash_report += self._dbg.involve_msec()
        self._crash_occurred = True

    def _debugger_worker_green(self):
        x = 3 # debug .... defaults to -> while True:
        while x > 1:
            self._create_testcases()
            for filename in os.listdir("testcases/"):
                output = ""
                process = subprocess.Popen(
                    "python debugging\\windbg.py -p \"" + self._program_path + "\" -t \"testcases\\" + filename + "\"",
                    stdout=subprocess.PIPE)
                self._logger.debug("Debugger started...")
                util = psutil.Process(process.pid)
                start = time.time()
                try:
                    while True:
                        if (time.time() - start > self._sleep_time) or (util.cpu_times() == 0):
                            break
                except:
                    pass # just ignore
                process.kill()
                output = process.stdout.read()
                if "Crash Report" in output:
                    self._logger.info("Crash")
                    self._report_queue.put(output)
                else:
                    self._logger.info("No crash")
                gevent.sleep(0)
                x -= 1

    def _create_testcases(self):
        for i in range(100):
            filename = "test" + str(i) if i > 9 else "test0" + str(i)
            filename += "." + self._fuzzer.file_type
            with open("testcases/" + filename, "w+") as fd:
                fd.write(self._fuzzer.fuzz())

    def _debugger_worker(self, filename):
        self._dbg.start_process("testcases/" + filename)
        self._dbg.run()
        self._create_crash_report()

    def start_worker(self):
        if self._greenlet is None:
            self._greenlet = gevent.spawn(self._debugger_worker_green)

    def stop_worker(self):
        if self._running:
            self._process.terminate()
            self._running = False

    def reset(self):
        self._greenlet = None
        self._testcase = ""
        self._crash_occurred = False
        self._crash_report = ""
        self._dbg.kill_process()

    @property
    def crashed(self):
        return self._crash_occurred

    @property
    def crash_report(self):
        return self._crash_report
