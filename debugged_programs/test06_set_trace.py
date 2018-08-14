# coding: utf-8
import sys

def dot():
    return 4


my_list = [1, 2, 3, 'cyril', 3.14 , False]

mon_dict = {
    'key1': "Cyril",
    'numbers': [1,2,3],
    'stephane': 16,
    dot: 6,
    'fun': dot,
    'fune': dot(),
}
print("mon_dict = %s" % mon_dict)

def sub():
    cs = "my Création exception"  # This is str with utf8 comment => Création§
    print(">>> %s: %s" % (type(cs), cs))
    if sys.version_info.major == 2:
        csu = unicode(cs, "utf_8")
        print(">>> type(csu)=%s" % type(csu))
    else:
        csu = cs
    python_version = sys.version_info[0]
    if sys.argv[1] == 'test_01_settrace':
        value_to_test_in_remote_client = 'set_trace_called'
        if python_version == 2:
            import ikpdb ; ikpdb.set_trace()
        elif python_version == 3:
            import ikp3db ; ikp3db.set_trace()
    
    elif sys.argv[1] == 'test_02_py37debugger_statement':
        if python_version == 2:
            import ikpdb ; ikpdb.set_trace()
        elif python_version == 3:
            value_to_test_in_remote_client = 'breakpoint_called'
            breakpoint()

if __name__ == '__main__':
    sub()
    print("That's All Folks")