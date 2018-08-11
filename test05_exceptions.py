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
DEBUGGED_PROGRAM = "debugged_programs/test05_exceptions.py"

class TestCase05Exceptions(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        pass    

    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        TESTED_DEBUGGER = os.environ.get('TESTED_DEBUGGER', '')
        if TESTED_DEBUGGER == 'ikp3db':
            PYTHON_EXEC = "py3xtests/bin/python"
        else:
            PYTHON_EXEC = "py27tests/bin/python"

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
            self.dp.kill()
            time.sleep(1)

    def test_01_unmanaged_exceptions(self):
        """Launch debugged program then check IKpdb break at exception.
        Check behaviour is correct with utf8 exception message.
        """
        time.sleep(0.5)  # allows debugger to start
        self.ikpdb.run_script()

        i_msg = self.ikpdb.receive()
        self.assertEqual(i_msg['command'], 
                         "programBreak", 
                         "Received: %s while expecting 'programBreak'" % (i_msg['command'],))
        self.assertEqual(i_msg['frames'][0]['line_number'], 
                         31, 
                         "Wrong exception catched.")
        self.assertEqual(i_msg['exception']['info'], 
                         unicode("my Création exception", 'utf_8'),
                         "Wrong exception catched.")
        self.ikpdb.resume()

    def test_02_resume_after_exception(self):
        """Launch debugged program then check IKpdb break at exception."""
        time.sleep(0.5)  # allows debugger to start
        self.ikpdb.run_script()

        i_msg = self.ikpdb.receive()
        self.assertEqual(i_msg['command'], 
                         "programBreak", 
                         "Received: %s while expecting 'programBreak'" % (i_msg['command'],))
        self.assertEqual(i_msg['frames'][0]['line_number'], 
                         31, 
                         "Wrong exception catched.")
        self.assertEqual(i_msg['exception']['info'], 
                         unicode("my Création exception", 'utf_8'),
                         "Wrong exception catched.")
        r = self.ikpdb.resume()
        i_msg = self.ikpdb.receive()
        self.assertEqual(i_msg['command'], 
                         "programEnd", 
                         "Received: %s while expecting 'programEnd'" % (i_msg['command'],))


