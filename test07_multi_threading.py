# coding: utf-8

import unittest
import os
import subprocess
import time
import socket
import logging
import json
from ikpdb_client import IKPdbClient

_logger = logging.getLogger(__file__)
_logger.addHandler(logging.StreamHandler())
_logger.setLevel(logging.INFO)



TESTED_IKPDB_HOST = '127.0.0.1'
TESTED_IKPDB_PORT = 15999
DEBUGGED_PROGRAM = "debugged_programs/test07_multi_threading.py"

class TestCase07MultiThreading(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        pass    

    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        TESTED_DEBUGGER = os.environ.get('TESTED_DEBUGGER', '')
        PYTHON_EXEC = "%s/bin/python" % os.environ.get('TESTED_PYTHON_VIRTUALENV', '')

        cmd_line = [
            PYTHON_EXEC, 
            "-m", TESTED_DEBUGGER, 
            #"--ikpdb-log=9NB",
            #"--ikpdb-log=9",
            "--ikpdb-port=%s" % TESTED_IKPDB_PORT,
            #"--ikpdb-welcome",
            DEBUGGED_PROGRAM,
            self._testMethodName 
        ]
        self.dp = subprocess.Popen(cmd_line, stdout=subprocess.PIPE)
        time.sleep(0.6)  # allows debugger to start
        self.ikpdb = IKPdbClient(TESTED_IKPDB_HOST, TESTED_IKPDB_PORT)

    def tearDown(self):
        if self.dp:
            proc_poll = self.dp.poll()
            if proc_poll is None:  # debugged prog did not exit
                self.dp.kill()
                time.sleep(1)


    def test_01_same_thread(self):
        """Launch debugged program with 2 threads and 1 breakpoint, step over
        10 times and check that it always breaks in the same thread."""
        time.sleep(0.5)  # allows debugger to start
        self.ikpdb.set_breakpoint(DEBUGGED_PROGRAM, line_number=42)
        self.ikpdb.run_script()
        debugged_thread = None
        debugged_thread_name = ''
        for i in range(10):
            
            i_msg = self.ikpdb.receive()
            self.assertEqual(i_msg['command'], 
                             "programBreak", 
                             "Received: %s while expecting 'programBreak'" % (i_msg['command'],))
            if debugged_thread is None:
                debugged_thread = i_msg['frames'][0]['thread']
                debugged_thread_name = i_msg['frames'][0].get('thread_name')
                print("thread_ident=%s, thread_name=%s" % (debugged_thread, debugged_thread_name,))
            else:
                print("thread_ident=%s, thread_name=%s" % (i_msg['frames'][0]['thread'], 
                                                           i_msg['frames'][0].get('thread_name'),))
                self.assertEqual(i_msg['frames'][0]['thread'], 
                                 debugged_thread,
                                 "Debugged thread has changed (i=%s, "
                                 "first_thread=%s:%s, last_thread=%s:%s)" % (
                                 i,
                                 debugged_thread, debugged_thread_name,
                                 i_msg['frames'][0]['thread'], i_msg['frames'][0].get('thread_name')))
            self.ikpdb.resume()


    def test_02_get_threads_list(self):
        """Launch debugged program with 2 threads and 1 breakpoint, break
        then get threads list().
        """
        time.sleep(0.5)  # allows debugger to start
        self.ikpdb.set_breakpoint(DEBUGGED_PROGRAM, line_number=42)
        self.ikpdb.run_script()

        i_msg = self.ikpdb.receive()
        self.assertEqual(i_msg['command'], 
                         "programBreak", 
                         "Received: %s while expecting 'programBreak'" % (i_msg['command'],))

        # TODO: evaluate "ikpdb.ikpdb.get_threads_list()"
        i_msg = self.ikpdb.evaluate(i_msg['frames'][0]['id'],
                                    "ikpdb.ikpdb.get_threads()")
        print(i_msg)
        # TODO: check 4 threads and Thread-1 et Threads2


    def test_03_switch_thread(self):
        """Launch debugged program with 2 threads and 1 breakpoint, step over
        5 times and check that it always breaks in the same thread."""
        time.sleep(0.5)  # allows debugger to start
        self.ikpdb.set_breakpoint(DEBUGGED_PROGRAM,
                                 line_number=42)

        self.ikpdb.run_script()
        debugged_thread = None
        debugged_thread_name = ''
        for i in range(5):
            i_msg = self.ikpdb.receive()
            self.assertEqual(i_msg['command'], 
                             "programBreak", 
                             "Received: %s while expecting 'programBreak'" % (i_msg['command'],))
            if debugged_thread is None:
                debugged_thread = i_msg['frames'][0]['thread']
                debugged_thread_name = i_msg['frames'][0].get('thread_name')
                print("thread_ident=%s, thread_name=%s" % (debugged_thread, debugged_thread_name,))
            else:
                print("thread_ident=%s, thread_name=%s" % (i_msg['frames'][0]['thread'], 
                                                           i_msg['frames'][0].get('thread_name'),))
                self.assertEqual(i_msg['frames'][0]['thread'], 
                                 debugged_thread,
                                 "Debugged thread has changed (i=%s, "
                                 "first_thread=%s:%s, last_thread=%s:%s)" % (
                                 i,
                                 debugged_thread, debugged_thread_name,
                                 i_msg['frames'][0]['thread'], i_msg['frames'][0].get('thread_name')))
            if i==4:
                pass
                # TODO: switcher le thread
            self.ikpdb.resume()


        # TODO: vérifie que l'on reste sur le thread2

