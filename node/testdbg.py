__author__ = 'susperius'

import debugging.windbg as wdbg
import worker.fuzzingworker as dbgworker
import gevent
import gevent.monkey
import time
import socket
from fuzzing.javascript import JsDomFuzz
from gevent.queue import Queue
from subprocess import Popen
import subprocess
import logging

gevent.monkey.patch_all()

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    fuz = JsDomFuzz(10, 1000, "ie")
    rep_q = Queue()
    #dbg_w = dbgworker.DebuggerWorker("C:\\Program Files\\Tracker Software\\PDF Viewer\\PDFXcview.exe\" -t \"testcases\\test.pdf", fuz, rep_q, 5)
    dbg_w = dbgworker.FuzzingWorker("C:\\Program Files\\Internet Explorer\\iexplore.exe", fuz, rep_q, 5, True)
    dbg_w.start_worker()
    gevent.sleep(20)
    rep = rep_q.get_nowait()
    print(rep)
    dbg_w.__create_testcases()
