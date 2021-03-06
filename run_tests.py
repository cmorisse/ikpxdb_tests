import sys
import os
import click

DO_TEST = False
if DO_TEST:
    from test01_launch import *
    from test02_breakpoints import *
    from test03_suspend import *
    from test03_2_suspend import *
    from test04_exit import *
    from test05_exceptions import *
    from test06_set_trace import *
else:
    from test07_multi_threading import *
    pass

def remove_launcher_options():
    sys.argv[:] = filter(lambda e: not e.startswith('--ikpxdb'), sys.argv)


@click.command()
@click.option('--ikpxdb_virtualenv', 
              default='py37venv',
              type=click.Choice(['py27venv', 'py36venv', 'py37venv']),
              help="Python used for tests.")
@click.option('--ikpxdb', 
              default='ikp3db', 
              type=click.Choice(['ikpdb', 'ikp3db']),
              help="Tested debugger.")
def launch_tests(ikpxdb, ikpxdb_virtualenv):
    os.environ['TESTED_DEBUGGER'] = ikpxdb
    os.environ['TESTED_PYTHON_VIRTUALENV'] = ikpxdb_virtualenv
    remove_launcher_options()
    
    print("\n")
    print("Tested debugger: '%s'" % ikpxdb)
    print("Tested python virtualenv: '%s'" % ikpxdb_virtualenv)
    print("\n\n")
    
    unittest.main(verbosity=2)


if __name__ == '__main__':
    launch_tests()