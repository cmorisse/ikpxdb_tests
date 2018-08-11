import sys
import os

from test01_launch import *
from test02_breakpoints import *
from test03_suspend import *
from test03_2_suspend import *
from test04_exit import *
from test05_exceptions import *


if __name__ == '__main__':
    try: 
       idx = sys.argv.index('__test_ikp3db')
       os.environ['TESTED_DEBUGGER'] = "ikp3db"
       del sys.argv[idx]
    except ValueError:
        pass

    if not os.environ.get('TESTED_DEBUGGER'):
        try: 
           idx = sys.argv.index('__test_ikpdb')
           os.environ['TESTED_DEBUGGER'] = "ikpdb"
           del sys.argv[idx]
        except ValueError:
            pass
        
    if not os.environ.get('TESTED_DEBUGGER'):
        print "Error: you must pass either '__test_ikp3db' or '__test_ikpdb' as a parameter."
        print("Aborting tests")
        sys.exit(1)

    unittest.main(verbosity=2)