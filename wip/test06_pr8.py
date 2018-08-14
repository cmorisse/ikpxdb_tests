#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 中文 --------------utf-8 characters-----------------
print("Hello")
while 1:
	a=[]  
	s = input()
	
	if s != "":
		for x in s.split():  
		    a.append(int(x))  
		   
		print(sum(a))
	else:
		break