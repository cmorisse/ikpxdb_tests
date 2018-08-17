# coding: utf-8

#
# This file is part of the IKPdb Debugger
# Copyright (c) 2016 by Cyril MORISSE, Audaxis
# Licence: MIT. See LICENCE at repository root
#
import sys
import os
import time
import threading
try:
    import ikpdb
except:
    import ikp3db as ikpdb


PYTHON_VERSION = sys.version_info[:2]
TEST_MULTI_THREADING = True
TEST_EXCEPTION_PROPAGATION = False
TEST_POSTMORTEM = True
TEST_SYS_EXIT = 0
TEST_STEPPING = False
TEST_SUSPEND = True


# Note that ikpdb.set_trace() will reset/mess breakpoints set using GUI
TEST_SET_TRACE = False  

TCB = TEST_CONDITIONAL_BREAKPOINT = True

class Worker(object):
    def __init__(self):
        self._running = True
    
    def terminate(self):
        self._running = False
        
    def run(self, n):
        work_count = 1
        while self._running and work_count <= n:
            print("Thread %s --> %s" % (threading.currentThread().getName(), work_count))
            time.sleep(0.2)
            work_count += 1
            if work_count == n:
                self.terminate()


if __name__=='__main__':

    TEST_DURATION_IN_SECONDS = 600

    w0 = Worker()
    thread_0 = threading.Thread(target=w0.run, args=(TEST_DURATION_IN_SECONDS*5,))
    thread_0.start()
    
    w1 = Worker()
    thread_1 = threading.Thread(target=w1.run, args=(TEST_DURATION_IN_SECONDS*5,))
    thread_1.start()

    thread_0.join()
    thread_1.join()

    print("finished")