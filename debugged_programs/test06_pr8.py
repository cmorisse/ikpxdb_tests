#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 中文 --------------utf-8 characters-----------------
import random
import string

# From https://stackoverflow.com/questions/45414818/how-to-generate-random-string
def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for m in range(length))

a = []

while True:
    s = random_string(45)
    
    if s != "":
        for x in list(s):
            print(x)
            a.append(ord(x))  
        break   
    else:
        break

print(sum(a))