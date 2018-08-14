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
DEBUGGED_PROGRAM = "debugged_programs/test06_set_trace.py"

class TestCase06setTrace(unittest.TestCase):
    
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
        time.sleep(0.5)  # allows debugger to exit (timeout loop=0.3s)


    def test_01_settrace(self):
        """Launch debugged program then check that it breaks at set_trace()"""
        time.sleep(0.5)  # allows debugger to start
        self.ikpdb.run_script()

        i_msg = self.ikpdb.receive()
        self.assertEqual(i_msg['command'], 
                         "programBreak", 
                         "Received: %s while expecting 'programBreak'" % (i_msg['command'],))
        remote_value = filter(lambda d: d['name']=='value_to_test_in_remote_client', i_msg['frames'][0]['f_locals'])[0]['value']
        self.assertEqual(remote_value,
                         "'set_trace_called'",
                         "Unexpected break (breakpoint() not called")
        remote_python_version = filter(lambda d: d['name']=='python_version', i_msg['frames'][0]['f_locals'])[0]['value']
        if remote_python_version == '2':
            self.assertEqual(i_msg['frames'][0]['line_number'], 
                             32,
                             "unexpected statement break.")
        else:
            self.assertEqual(i_msg['frames'][0]['line_number'], 
                             34,
                             "unexpected statement break.")

        self.ikpdb.resume()
        i_msg = self.ikpdb.receive()
        self.assertEqual(i_msg['command'], 
                         "programEnd", 
                         "Received: %s while expecting 'programEnd'" % (i_msg['command'],))

    def test_02_py37debugger_statement(self):
        """Launch debugged program then check IKpdb break at debugger() statement"""
        time.sleep(0.5)  # allows debugger to start
        self.ikpdb.run_script()

        i_msg = self.ikpdb.receive()
        self.assertEqual(i_msg['command'], 
                         "programBreak", 
                         "Received: %s while expecting 'programBreak'" % (i_msg['command'],))
        remote_python_version = filter(lambda d: d['name']=='python_version', i_msg['frames'][0]['f_locals'])[0]['value']
        if remote_python_version == '3':
            remote_value = filter(lambda d: d['name']=='value_to_test_in_remote_client', i_msg['frames'][0]['f_locals'])[0]['value']
            self.assertEqual(remote_value,
                             "'breakpoint_called'",
                             "Unexpected break (breakpoint() not called")
            self.assertEqual(i_msg['frames'][0]['line_number'], 
                             41,
                             "unexpected statement break.")
        else:
            self.assertEqual(i_msg['frames'][0]['line_number'], 
                             38,
                             "unexpected statement break.")
        r = self.ikpdb.resume()
        i_msg = self.ikpdb.receive()
        self.assertEqual(i_msg['command'], 
                         "programEnd", 
                         "Received: %s while expecting 'programEnd'" % (i_msg['command'],))


