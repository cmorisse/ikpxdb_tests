
        ______ __ ____           ____       __            __      
       /  _/ //_// __ \_  ______/ / /_     / /____  _____/ /______
       / // ,<  / /_/ / |/_/ __  / __ \   / __/ _ \/ ___/ __/ ___/
     _/ // /| |/ ____/>  </ /_/ / /_/ /  / /_/  __(__  ) /_(__  ) 
    /___/_/ |_/_/   /_/|_|\__,_/_.___/   \__/\___/____/\__/____/  
    ===========================================================
   

License
=======

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
    
Launch tests
============

    # in the ikpdxdb_tests directory
    py27tests/bin/python 
    py27tests/bin/python run_tests.py --help


Development
===========

The tests can be debugged (client side) using IKPdb.


