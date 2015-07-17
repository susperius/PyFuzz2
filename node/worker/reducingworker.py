__author__ = 'susperius'

from worker import Worker
import gevent
import logging
import subprocess
import os
from reportworker import ReportWorker


class ReducingWorker(Worker):
    def __init__(self, reducer, program_path, sleep_time, dbg_child, report_queue):
        self._program_path = program_path
        self._sleep_time = sleep_time
        self._running = False
        self._greenlet = None
        self._logger = logging.getLogger(__name__)
        self._reducer = reducer
        self._process = None
        self._dbg_child = dbg_child
        self._report_queue = report_queue

    def __worker_green(self):
        case = self._reducer.reduce()
        maj_hash, min_hash = self.__get_report_hashes(self._reducer.crash_report)
        while case is not None:
            if self._reducer.NAME == 'js_reducer':
                with open('tmp/reduced.html', 'wb+') as fd:
                    fd.write(case)
                self._process = subprocess.Popen(
                            "python debugging\\windbg.py -p \"" + self._program_path
                            + "\" -t \"http://127.0.0.1:8080/reduced.html\" -c " + str(self._dbg_child),
                            stdout=subprocess.PIPE)
                gevent.sleep(self._sleep_time)
                self._process.kill()
                if os.path.isfile("tmp_crash_report"):
                    with open("tmp_crash_report") as fd:
                        output = fd.read()
                    os.remove("tmp_crash_report")
                    red_maj_hash, red_min_hash = self.__get_report_hashes(output)
                    if red_maj_hash == maj_hash:
                        self._reducer.crashed(True)
                        with open('red_crash_file.'+self._reducer.file_type, 'wb+') as case_fd, open('red_crash_report.txt', 'wb+') as output_fd:
                            case_fd.write(case)
                            output_fd.write(output)
                        if red_min_hash != min_hash:
                            self._report_queue.put((0xFF, (output, case)))
                    else:
                        self._reducer.crashed(False)
                        self._report_queue.put((0xFF, (output, case)))

                else:
                    self._reducer.crashed(False)
                os.remove('tmp/reduced.html')
            case = self._reducer.reduce()
        self._logger.info('Reduced the Testcase!')
        quit()



    def stop_worker(self):
        if self._running:
            self._running = False
            gevent.kill(self._greenlet)

    def start_worker(self):
        if not self._running:
            self._running = True
            self._greenlet = gevent.spawn(self.__worker_green)

    @staticmethod
    def __get_report_hashes(report):
        hash_val = ReportWorker.parse_string_report(report, "(Hash=", ")")
        hash_val = hash_val.split('.')
        return hash_val[0], hash_val[1]
