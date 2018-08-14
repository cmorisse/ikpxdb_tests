
        ______ __ ____           ____       __            __      
       /  _/ //_// __ \_  ______/ / /_     / /____  _____/ /______
       / // ,<  / /_/ / |/_/ __  / __ \   / __/ _ \/ ___/ __/ ___/
     _/ // /| |/ ____/>  </ /_/ / /_/ /  / /_/  __(__  ) /_(__  ) 
    /___/_/ |_/_/   /_/|_|\__,_/_.___/   \__/\___/____/\__/____/  
    ===========================================================
   

Introduction
============

This repository allows to test IKPdb and IKP3db against several python versions:
* python 2
* python 3.6
* python 3.7

All tests are done via IKPdb network protocol used by debugger client.

`ìkpdb_client.py` contains a basic network client for IKPdb.

The tests are written in Python 2. 
So this repository contains a Test suite written in python 2 that can test
python 2 or python 3 version of IKPdb via it's network protocol.

License
-------

All files in this repo are Licensed under MIT.


Installation
============

    git clone git@github.com:cmorisse/ikpxdb_tests.git
    cd ikpxdb_tests

    # in the ikpdxdb_tests directory
    virtualenv --python=python2 py27venv
    # Choose one among these
    py27venv/bin/pip install click
    py27venv/bin/pip install ikpdb
    py27venv/bin/pip install -e ../ikpdb

    # warning python 3.6 minimum
    virtualenv --python=python3 py36venv
    # Choose one among these
    py36venv/bin/pip install ikp3db
    py36venv/bin/pip install -e ../ikp3db


Note that IKPdbs versions must be installed in virtualenv named after py99venv.
This contraint is inforced by run_test.py.


Launch tests
============

    # in the ikpdxdb_tests directory
    py27tests/bin/python run_tests.py --help

Test launcher use 2 parameters to define the tests to run:

* `--ikpxdb` defines the debugger to test (ikpdb or ikp3db)
* `--ikpxdb_virtualenv` defines python virtual hence python version to test

Default values allows to test newest python version supported.


Development
===========

The tests can be debugged (client side) using IKPdb.


