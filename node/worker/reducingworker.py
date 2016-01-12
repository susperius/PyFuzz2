from worker import Worker
import gevent
import logging
import subprocess
import psutil
import os
import re
from reportworker import ReportWorker

__author__ = 'susperius'

WAIT_FOR_PROCESSES_TO_SPAWN = 2


class ReducingWorker(Worker):
    def __init__(self, reducer, programs, report_queue):
        self._programs = programs
        self._need_web_server = False
        for prog in self._programs:
            if bool(prog['use_http']):
                self._need_web_server = True
        self._running = False
        self._greenlet = None
        self._logger = logging.getLogger(__name__)
        self._reducer = reducer
        self._processes = []
        self._report_queue = report_queue
        self._actual_file = {}
        self._web_process = None
        self._DEVNULL = os.open(os.devnull, os.O_RDWR)

    def __worker_green(self):
        results = self.__get_all_crash_results()
        self._logger.debug("Found " + str(len(results)) + " crashes")
        for crash in results:
            program = None
            for prog in self._programs:
                if prog['name'] == crash['program_name']:
                    program = prog
                    self._logger.debug("Found program: " + program['name'])
            if program is None:
                continue
            if bool(program['use_http']):
                self._web_process = subprocess.Popen("python -m SimpleHTTPServer 8080", stdout=self._DEVNULL,
                                                     stderr=self._DEVNULL, cwd=crash['directory'])
            crashed = False
            for i in range(3):
                crashed = self.__check_for_crash(crash['crash_file'], crash, program)
                if crashed:
                    os.remove("tmp_crash_report")
                    self._logger.info("Crash file verified")
                    break
            if not crashed:
                self._logger.info("Crash file seems to be a false positive: " + crash['directory'] + "\\" + crash['crash_file'])
                continue
            self._reducer.set_case(crash['directory'] + "/", crash['crash_file'], crash['report'])
            original_report = self._reducer.crash_report
            original_maj_hash, original_min_hash = self.__get_report_hashes(original_report)
            reduced_crash = None
            reduced_crash_report = None
            reduced_crash_min_hash = None
            reduced_case = self._reducer.reduce()
            testcase = []
            for file_name in crash['additional_files']:
                with open(crash['directory'] + "/" + file_name, 'rb') as fd:
                    testcase.append((file_name, fd.read()))
            self._logger.info("Starting test case reduction ...")
            while reduced_case is not None:
                self.__write_reduced_case(crash['directory'] + "/", reduced_case)
                if self.__check_for_crash("reduced." + self._reducer.file_type, crash, program):
                    with open("tmp_crash_report") as fd:
                        reduced_case_report = fd.read()
                    os.remove("tmp_crash_report")
                    reduced_maj_hash, reduced_min_hash = self.__get_report_hashes(reduced_case_report)
                    if reduced_maj_hash == original_maj_hash:  # The same crash
                        self._logger.debug("Reducing crash!")
                        reduced_crash = reduced_case
                        reduced_crash_report = reduced_case_report
                        reduced_crash_min_hash = reduced_min_hash
                        self._reducer.crashed(True)
                    else:  # A new crash has appeared
                        self._logger.info("Found a new unique crash!")
                        testcase.append(("test" + reduced_maj_hash + self._reducer.file_type, reduced_case))
                        self._report_queue.put((0xFF, (program['name'], reduced_case_report, testcase)))
                        self._reducer.crashed(False)
                else:
                    self._reducer.crashed(False)
                reduced_case = self._reducer.reduce()
            if reduced_crash is not None:
                reduced_crash_report = re.sub(reduced_crash_min_hash, "0x00000000", reduced_crash_report)
                testcase.append(reduced_case)
                self._report_queue.put((0xFF, (program['name'], reduced_crash_report, testcase)))
        self._logger.info("Reducing completed ...")
        quit()

    def __check_for_crash(self, filename, crash, program):
        if bool(program['use_http']):
            self._processes.append(subprocess.Popen(
                    "python debugging\\windbg.py -p \"" + program['path']
                    + "\" -t \"http://127.0.0.1:8080/" + filename + "\" -X",
                    stdout=self._DEVNULL, stderr=self._DEVNULL))
        else:
            self._processes.append(subprocess.Popen(
                    "python debugging\\windbg.py -p \"" + program['path']
                    + "\" -t \"" + os.getcwd() + crash['directory'] + filename +
                    "\" -X", stdout=self._DEVNULL, stderr=self._DEVNULL))
        gevent.sleep(int(program['sleep_time']))
        self.__kill_processes()
        self._processes = []
        if os.path.isfile("tmp_crash_report"):
            return True
        else:
            return False

    def __write_reduced_case(self, directory, reduced_case):
        with open(directory + "reduced." + self._reducer.file_type, 'wb+') as fd:
            fd.write(reduced_case)

    def __get_all_crash_results(self):
        results = []
        for dir_name, sub_dir_list, file_list in os.walk("results"):
            if file_list and "__init__.py" not in file_list:
                crash_file = ""
                crash_report = ""
                additional_files = []
                for file_name in file_list:
                    if self._reducer.file_type in file_name:
                        crash_file = file_name
                    elif "txt" in file_name:
                        crash_report = file_name
                    else:
                        additional_files.append(file_name)
                results.append({'crash_file': crash_file, 'report': crash_report, 'directory': dir_name,
                                'program_name': dir_name.split("\\")[1], 'additional_files': additional_files})
        return results

    def __kill_processes(self):
        for proc in self._processes:
            try:
                proc.kill()
            except psutil.NoSuchProcess:
                pass

    def stop_worker(self):
        if self._running:
            self._running = False
            gevent.kill(self._greenlet)
            try:
                with open(self._reducer.path + self._actual_file['origin'][0], 'wb+') as case_fd, open(
                            self._reducer.path + self._actual_file['origin'][1], 'w+') as report_fd:
                    case_fd.write(self._actual_file['case'][0])
                    report_fd.write(self._actual_file['case'][1])
            except:
                pass  # Just ignore perhaps there is in this moment no reduced file

    def start_worker(self):
        if not self._running:
            self._running = True
            self._greenlet = gevent.spawn(self.__worker_green)

    @staticmethod
    def __get_report_hashes(report):
        hash_val = ReportWorker.parse_string_report(report, "(Hash=", ")")
        hash_val = hash_val.split('.')
        return hash_val[0], hash_val[1]

    @staticmethod
    def __get_short_description(report):
        return ReportWorker.parse_string_report(report, "Short Description: ", "\r")
