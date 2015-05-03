__author__ = 'susperius'

import gevent
import os
import time
import psutil
from multiprocessing import Process
from debugging.windbg import Debugger


class DebuggerWorker:
    def __init__(self, dbg, fuzzer, report_queue, sleep_time):
        self._greenlet = None
        self._process = None
        self._running = False
        self._dbg = dbg
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
        while True:
            self._create_testcases()
            for filename in os.listdir("testcases/"):
                self._process = Process(target=self._debugger_worker_green, args=filename)
                self._process.start()
                started = time.time()
                util = psutil.Process(self._process.pid)
                if (time.time() - started >= self._sleep_time) or (util.get_cpu_times == 0):
                    # Either time is up or no cpu time is used
                    self._process.terminate()
                if self.crashed:
                    self._report_queue.put(self.crash_report)
                    self._crash_occurred = False

    def _create_testcases(self):
        pass

    def _debugger_worker(self, filename):
        self._dbg.start_process("testcases/"+filename)
        self._dbg.run()
        self._create_crash_report()

    def start_worker(self, testcase):
        if self._greenlet is None:
            self._greenlet = gevent.spawn(self._debugger_worker_green)
        if not self._running:
            self._testcase = testcase
            self._process = Process(target=self._debugger_worker_green)
            self._process.start()
            self._running = True

    def stop_worker(self):
        if self._running:
            self._process.terminate()
            self._running = False

    def reset(self):
        self._process = None
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
