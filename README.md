        ______ __ ____      ____       __            __      
       /  _/ //_// __ \____/ / /_     / /____  _____/ /______
       / // ,<  / /_/ / __  / __ \   / __/ _ \/ ___/ __/ ___/
     _/ // /| |/ ____/ /_/ / /_/ /  / /_/  __(__  ) /_(__  ) 
    /___/_/ |_/_/    \__,_/_.___/   \__/\___/____/\__/____/  
    =======================================================
   

License
=======

All files in this repo are Licensed under MIT.


 Installation
 ============
 
 
    git clone ...
    cd ikpxdb_tests
    
    # in the ikpdxdb_tests
    virtualenv --python=python2 py27tests
    source py27tests/bin/activate
    # Choose one among these
    pip install ikpdb
    pip install -e ../ikpdb
    deactivate
    
    # warning python 3.6 minimum
    virtualenv --python=python3 py3xtests
    source py3xtests/bin/activate
    # Choose one among these
    pip install ikp3db
    pip install -e ../ikp3db
    deactivate
    
    
Launch tests
============

    cd ikpxdb_tests
    python run_tests __test_ikpdb  # for ikpdb 
    # or 
    python run_tests __test_ikp3db


Development
===========

The tests can be debugged (client side) using IKPdb.


