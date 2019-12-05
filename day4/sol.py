#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import math

# Should have used the "any" function...

# Realized later that this could be as simple as sorting and comparing
def increasing(n):
	s = str(n)
	low = 0
	for c in s:
		nextnum = int(c)
		if nextnum < low:
			return False
		else:
			low = nextnum
	return True

def twoadj(n):
	s = str(n)
	for i in range(len(s) - 1):
		if s[i] == s[i + 1]:
			return True
	return False

def onlytwoadj(n):
	s = str(n)
	curr = s[0]
	tot = 0
	acc = ""
	for i in range(len(s)):
		if s[i] == curr:
			tot += 1
		else:
			acc += str(tot)
			tot = 1
			curr = s[i]
	acc += str(tot)
	return "2" in acc

fn = "./in.txt"
l = util.filetolist(fn)[0]
num1 = int(l[0:6])
num2 = int(l[7:])

p1 = 0
p2 = 0
for i in range(num1, num2+1):
	if increasing(i) and twoadj(i):
		p1 += 1
	if increasing(i) and onlytwoadj(i):
		p2 += 1

print("Part 1")
print(p1)
print("Part 2")
print(p2)