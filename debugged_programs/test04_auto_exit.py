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
    # IKpdb should exit even if we don't call exit.
    # That's a long standing bug. This will remind us until we fix it.
    # sys.exit(27)
