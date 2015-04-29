__author__ = 'susperius'

import gevent
from debugging.windbg import Debugger


class DebuggerWorker:
    def __init__(self, dbg):
        self._greenlet = None
        self._dbg = dbg
        self._testcase = ""
        self._crash_occurred = False
        self._crash_report = ""

    def _create_crash_report(self):
        self._crash_report += "Crash Report\r\n"
        self._crash_report += self._dbg.issue_dbg_command(u"r")
        self._crash_report += "\r\n"
        self._crash_report += self._dbg.issue_dbg_command(u"k")
        self._crash_report += "\r\n"
        self._crash_report += self._dbg.involve_msec()

    def _debugger_worker_green(self):
        self._dbg.start_process(self._testcase)
        self._dbg.run()
        self._create_crash_report()
        gevent.sleep(0)

    def start_worker(self, testcase):
        if self._greenlet is None:
            self._testcase = testcase
            self._greenlet = gevent.spawn(self._debugger_worker_green)
            gevent.sleep(0)

    def stop_worker(self):
        if self._greenlet is not None:
            gevent.kill(self._greenlet)
            self._greenlet = None

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
