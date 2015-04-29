__author__ = 'susperius'

import debugging.windbg as wdbg
import worker.debuggerworker as dbgworker
import gevent
import time
import socket

dbg = wdbg.Debugger("C:\\Program Files\\Tracker Software\\PDF Viewer\\PDFXcview.exe")


dbg_w = dbgworker.DebuggerWorker(dbg)

dbg_w.start_worker("test.pdf")

gevent.sleep(5)

print(dbg_w.crash_report)

dbg_w.reset()