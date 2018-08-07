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
        print(">>> %s: %s" % (type(csu), csu))
    else:
        csu = cs
    
    if True:
        raise Exception(csu)
    #raise Exception(cs)


if __name__ == '__main__':
    sub()
    print("That's All Folks")