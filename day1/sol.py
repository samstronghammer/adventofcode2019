#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import math

def f(x):
	return math.floor(x / 3) - 2

def getmass(x):
	if f(x) < 0:
		return 0
	else:
		return f(x) + getmass(f(x))
		
intlist = util.filetointlist("./in.txt")
p1 = list(map(lambda x: f(x), intlist))
p2 = list(map(lambda x: getmass(x), intlist))
print(sum(p1))
print(sum(p2))
