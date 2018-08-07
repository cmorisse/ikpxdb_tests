from __future__ import print_function
import time
import sys

def looping_function():
    loop = 0
    while loop < 7:
        
        print("loop=%s, " % loop, end='')
        time.sleep(0.2)
        loop += 1
    print()

if __name__ == '__main__':
    looping_function()
    # Bu calling sys.exit() we force IKPdb to quit and thus exit command_loop
    # See test04_auto_exit.py for a long standing bug
    sys.exit(27)
