import time
import ikpdb
import sys

class BogoException(Exception):
    pass


def looping_function():
    loop = 0
    while loop < 10:
        print("loop=%s" % loop)
        time.sleep(0.2)
        loop += 1
    #ikpdb.set_trace()
    #raise BogoException("Waf")

if __name__ == '__main__':
    looping_function()
    sys.exit(0)