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
DEBUGGED_PROGRAM = "debugged_programs/test03_2_suspend.py"

class TestCase03Suspend(unittest.TestCase):
    
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
            #"--ikpdb-log=9NX",
            #"--ikpdb-log=9X",
            #"--ikpdb-log=9",
            "--ikpdb-port=%s" % TESTED_IKPDB_PORT,
            #"--ikpdb-welcome",
            DEBUGGED_PROGRAM,
            "t02" 
        ]
        # uncomment to monitor debugged program output
        #self.dp = subprocess.Popen(cmd_line)
        self.dp = subprocess.Popen(cmd_line, stdout=subprocess.PIPE)
        
        time.sleep(0.4)  # allows debugger to start
        self.ikpdb = IKPdbClient(TESTED_IKPDB_HOST, TESTED_IKPDB_PORT)

    def tearDown(self):
        if self.dp:
            self.dp.kill()
            time.sleep(1)

    def test_01_suspend(self):
        """Launch a debugged program and suspend / resume twice (github #7)."""
        time.sleep(0.2)  # allows debugger to start
        self.ikpdb.run_script()

        time.sleep(1)  # allow running program to loop for 2s
        msg_id = self.ikpdb.suspend()
        try:
            i_msg = self.ikpdb.receive(2)
            self.assertEqual(i_msg['command'], 'programBreak', "Unexpected reply to 'suspend'.")
        except socket.timeout:
            self.assertFalse(True, "IKPdb never suspended (timeout).")

        time.sleep(1)
        msg_id = self.ikpdb.resume()

        time.sleep(1)  # allow running program to loop for 1s
        msg_id = self.ikpdb.suspend()
        try:
            i_msg = self.ikpdb.receive(2)
            self.assertEqual(i_msg['command'], 'programBreak', "Unexpected reply to 'suspend'.")
        except socket.timeout:
            self.assertFalse(True, "IKPdb never suspended (timeout).")
            

