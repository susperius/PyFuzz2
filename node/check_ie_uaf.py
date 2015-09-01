__author__ = 'susperius'
"""
 This little helper is meant to support u filter the ReadAVNearNull or WriteAVNearNull.
 You give a path with your crash cases you want to analyze and the helper starts them
 with a "on-the-fly patched" protected free.
 In the protected free the memset value is changed to 0xFF. So you can easily see, if a freed
 object is used.
"""

from optparse import OptionParser
import os
import subprocess
from time import sleep

BREAKPOINT = "bp mshtml + 7418a 'ed esp ffffffff; g'"
SLEEP_TIME = 10
DIRECTORY = "results"
PROGRAM_PATH = "C:\Program Files\Internet Explorer\iexplore.exe"

if __name__ == "__main__":
    for dir_path, dirs, files in os.walk(DIRECTORY):
        for single_file in files:
            if single_file.endswith("html"):
                test_path = os.path.join(os.getcwd(), os.path.join(dir_path, single_file))
                print("[*] Test case: " + test_path)
                process = subprocess.Popen("python debugging\\windbg.py -p \"" + PROGRAM_PATH + "\" -t \"" +
                                           test_path + "\" -c True -i \"" + BREAKPOINT + "\"", stdout=subprocess.PIPE)
                sleep(10)
                if os.path.isfile("tmp_crash_report"):
                    with open("tmp_crash_report", "rb") as fd:
                        report = fd.read()
                    if "NearNull" not in report:
                        print("[+] Possible UAF\r\n")
                        os.makedirs("results/interesting_ie") if not os.path.exists("results/interesting_ie") else None
                        with open(dir_path + single_file, 'rb') as test_fd:
                            test = test_fd.read()
                        with open("results/interesting_ie/" + single_file, 'wb+') as test_fd, \
                                open("results/interesting_ie/" + single_file + "_report.txt", 'wb+') as report_fd:
                            test_fd.write(test)
                            report_fd.write(report)
                    else:
                        print("[-] No UAF\r\n")
                else:
                    print("[-] No Crash")
                process.kill()

