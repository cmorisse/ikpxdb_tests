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
        """Launch debugged program with 2 threads and 1 breakpoint, break, resume
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
        then send getThreads command.
        """
        time.sleep(0.5)  # allows debugger to start
        self.ikpdb.set_breakpoint(DEBUGGED_PROGRAM, line_number=42)
        self.ikpdb.run_script()

        i_msg = self.ikpdb.receive()
        self.assertEqual(i_msg['command'],
                         "programBreak", 
                         "Received: %s while expecting 'programBreak'" % (i_msg['command'],))

        i_msg = self.ikpdb.get_threads()
        threads_dict = i_msg['result']
        nb_threads = len(threads_dict)
        self.assertEqual(nb_threads, 4, 
                         "Unexpected number of threads (Received: %s, expecting 4)" % (nb_threads,))
        self.assertEqual(set([threads_dict[ident]['name'] for ident in threads_dict]),
                        set([u'Thread-2', u'IKPdbCommandLoop', u'MainThread', u'Thread-1']),
                        "Incorrect threads list returned.")

    def test_03_set_debugged_thread_none(self):
        """Launch debugged program with 2 threads and 1 breakpoint, break
        then call setDebuggedThread(None).
        """
        time.sleep(0.5)  # allows debugger to start
        self.ikpdb.set_breakpoint(DEBUGGED_PROGRAM, line_number=42)
        self.ikpdb.run_script()

        i_msg = self.ikpdb.receive()
        self.assertEqual(i_msg['command'],
                         "programBreak", 
                         "Received: %s while expecting 'programBreak'" % (i_msg['command'],))

        threads_dict = self.ikpdb.get_threads()['result']
        
        i_msg = self.ikpdb.set_debugged_thread(None)
        threads_dict = i_msg['result']
        nb_threads = len(threads_dict)
        self.assertEqual(nb_threads, 4, 
                         "Unexpected number of threads (Received: %s, expecting 4)" % (nb_threads,))
        self.assertEqual(set([threads_dict[ident]['name'] for ident in threads_dict]),
                        set([u'Thread-2', u'IKPdbCommandLoop', u'MainThread', u'Thread-1']),
                        "Incorrect threads list returned.")

    def test_04_set_debugged_thread_ikpdb(self):
        """Launch debugged program with 2 threads and 1 breakpoint, break
        then call setDebuggedThread('IKPDBCommandLoop thread ident').
        """
        time.sleep(0.5)  # allows debugger to start
        self.ikpdb.set_breakpoint(DEBUGGED_PROGRAM, line_number=42)
        self.ikpdb.run_script()

        i_msg = self.ikpdb.receive()
        self.assertEqual(i_msg['command'],
                         "programBreak", 
                         "Received: %s while expecting 'programBreak'" % (i_msg['command'],))

        threads_dict = self.ikpdb.get_threads()['result']
        ikpdb_thread_ident = filter(lambda t: t['name'].startswith("IKPdbCommandLoop"), [threads_dict[ident] for ident in threads_dict])[0]['ident']
        reply = self.ikpdb.set_debugged_thread(ikpdb_thread_ident)
        
        self.assertEqual(reply['commandExecStatus'], 'error', 
                         "setDebuggedThread(IKPdbCommandLoop) should have failed.")
        self.assertTrue(reply['error_messages'][0].startswith("Cannot debug IKPdb tracer"),
                        "Wrong error message received for setDebuggedThread(IKPdbCommandLoop).")

    def test_05_set_debugged_thread_wrong_thident(self):
        """Launch debugged program with 2 threads and 1 breakpoint, break
        then call setDebuggedThread(wrong thread ident).
        """
        time.sleep(0.5)  # allows debugger to start
        self.ikpdb.set_breakpoint(DEBUGGED_PROGRAM, line_number=42)
        self.ikpdb.run_script()

        i_msg = self.ikpdb.receive()
        self.assertEqual(i_msg['command'],
                         "programBreak", 
                         "Received: %s while expecting 'programBreak'" % (i_msg['command'],))

        threads_dict = self.ikpdb.get_threads()['result']
        wrong_thread_ident = 999999999000
        reply = self.ikpdb.set_debugged_thread(wrong_thread_ident)
        
        self.assertEqual(reply['commandExecStatus'], 'error', 
                         "setDebuggedThread(wrong_thread_ident) should have failed.")
        self.assertTrue(reply['error_messages'][0].startswith("No thread with ident:"),
                        "Wrong error message received for setDebuggedThread(IKPdbCommandLoop).")

    def test_06_switch_thread(self):
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
                threads_dict = i_msg['threads']
                test_threads = {td['name']:td['ident'] for td in filter(lambda t: t['name'].startswith("Thread-"), [threads_dict[ident] for ident in threads_dict])}
                if debugged_thread_name == 'Thread-1':
                    next_thread_ident = test_threads['Thread-2']
                    next_thread_name = 'Thread-2'
                else:
                    next_thread_ident = test_threads['Thread-1']
                    next_thread_name = 'Thread-1'
                print("Switching to thread: %s, %s" % (next_thread_ident, next_thread_name))
                reply = self.ikpdb.set_debugged_thread(next_thread_ident)
            self.ikpdb.resume()


        for i in range(5):
            i_msg = self.ikpdb.receive()
            self.assertEqual(i_msg['command'], 
                             "programBreak", 
                             "Received: %s while expecting 'programBreak'" % (i_msg['command'],))
            print("thread_ident=%s, thread_name=%s" % (i_msg['frames'][0]['thread'], 
                                                           i_msg['frames'][0].get('thread_name'),))
            self.assertEqual(i_msg['frames'][0]['thread'], 
                             next_thread_ident,
                             "Debugged thread has changed (i=%s, "
                             "first_thread=%s:%s, last_thread=%s:%s)" % (
                             i,
                             debugged_thread, debugged_thread_name,
                             i_msg['frames'][0]['thread'], i_msg['frames'][0].get('thread_name')))
            self.ikpdb.resume()

