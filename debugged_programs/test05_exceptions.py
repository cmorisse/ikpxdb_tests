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
    
    if sys.argv[1] in ('test_01_unmanaged_exceptions', 
                       'test_02_resume_after_exception'):
        raise Exception(csu)


if __name__ == '__main__':
    sub()
    print("That's All Folks")