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
DEBUGGED_PROGRAM = "debugged_programs/test04_exit.py"

class TestCase04Exit(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        pass    

    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        TESTED_DEBUGGER = os.environ.get('TESTED_DEBUGGER', '')
        PYTHON_EXEC = "%s/bin/python" % os.environ.get('TESTED_PYTHON_VIRTUALENV', '')
        
        if self._testMethodName == 'test_01_exit':
            DEBUGGED_PROGRAM = "debugged_programs/test04_exit.py"
        if self._testMethodName == 'test_02_autoexit':
            DEBUGGED_PROGRAM = "debugged_programs/test04_auto_exit.py"

        cmd_line = [
            PYTHON_EXEC, 
            "-m", TESTED_DEBUGGER, 
            #"--ikpdb-log=9NB",
            #"--ikpdb-log=9",
            "--ikpdb-port=%s" % TESTED_IKPDB_PORT,
            #"--ikpdb-welcome",
            DEBUGGED_PROGRAM,
            "t02" 
        ]
        self.dp = subprocess.Popen(cmd_line, stdout=subprocess.PIPE)
        time.sleep(0.6)  # allows debugger to start
        self.ikpdb = IKPdbClient(TESTED_IKPDB_HOST, TESTED_IKPDB_PORT)

    def tearDown(self):
        if self.dp:
            # to allow tests to support handling of autoexit until fixed in 
            # both versions
            proc_poll = self.dp.poll()
            if proc_poll is None: 
                self.dp.kill()
                time.sleep(1)

    def test_01_exit(self):
        """Launch a debugged program and check IKpdb exit when sys.exit() is called."""
        time.sleep(0.5)  # allows debugger to start
        self.ikpdb.run_script()

        time.sleep(2)  # allow running program to loop for 2s
        i_msg = self.ikpdb.receive(7)
        self.assertEqual(i_msg['command'], 
                         "programEnd", 
                         "Received: %s while expecting 'programEnd'" % (i_msg['command'],))
        
        time.sleep(3)
        # see https://stackoverflow.com/questions/43274476/is-there-a-way-to-check-if-a-subprocess-is-still-running
        proc_poll = self.dp.poll()
        self.assertIsNotNone(proc_poll, "IKPdb never exited")

    def test_02_autoexit(self):
        """Launch a debugged program and check IKpdb exit even if sys.exit() is NOT called."""
        time.sleep(0.5)  # allows debugger to start
        self.ikpdb.run_script()

        time.sleep(2)  # allow running program to loop for 2s
        i_msg = self.ikpdb.receive(7)
        self.assertEqual(i_msg['command'], 
                         "programEnd", 
                         "Received: %s while expecting 'programEnd'" % (i_msg['command'],))
        
        time.sleep(3)
        # see https://stackoverflow.com/questions/43274476/is-there-a-way-to-check-if-a-subprocess-is-still-running
        proc_poll = self.dp.poll()
        self.assertIsNotNone(proc_poll, "IKPdb never exited")
