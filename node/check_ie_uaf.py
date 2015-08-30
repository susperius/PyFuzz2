__author__ = 'susperius'
"""
 This little helper is meant to support u filter the ReadAVNearNull or WriteAVNearNull.
 You give a path with your crash cases you want to analyze and the helper starts them
 with a "on-the-fly patched" protected free.
 In the protected free the memset value is changed to 0xFF. So you can easily see, if a freed
 object is used.
"""

from optparse import OptionParser

BREAKPOINT_OFFSET = "mshtml + x"