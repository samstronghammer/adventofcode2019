#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import math

# Hands down the *best* challenge so far! I loved the punch line. Part two of this
# challenge was close to my best so far. A couple of hard-to-find typos cost me
# a lot of time in part 1. With additional code cleaning I could remove the 
# superfluous computation in steps_till_index_repeats (or even keep going till
# all of the indexes repeat at some point, that could cut the computation time
# by 2/3).


# I borrowed these two from https://www.programiz.com/python-programming/examples/lcm
def gcd(x, y):
   while(y):
       x, y = y, x % y
   return x

def lcm(x, y):
   lcm = (x*y) // gcd(x,y)
   return lcm

def gravity(m1, m2):
	assert m1[0] != m2[0]
	for i in range(3):
		if m1[1][i] < m2[1][i]:
			m1[2][i] += 1
			m2[2][i] -= 1
		elif m1[1][i] > m2[1][i]:
			m1[2][i] -= 1
			m2[2][i] += 1

def total_energy(m):
	return sum([abs(x) for x in m[1]]) * sum([abs(x) for x in m[2]])

def new_universe():
	fn = "./in.txt"
	l2 = util.filetowordlist(fn)
	l = []
	idval = 0
	for ln in l2:
		sp = ln.split(",")
		x = int(sp[0].split("=")[1])
		y = int(sp[1].split("=")[1])
		z = int(sp[2].split("=")[1][:-1])
		l.append([idval, [x, y, z], [0, 0, 0]])
		idval += 1
	return l

def steps_till_index_repeats(index):
	l = new_universe()
	prevstates = set()
	steps_taken = 0
	while True:
		universe_tuple = tuple([(m[0], m[1][index], m[2][index]) for m in l])
		if universe_tuple in prevstates:
			break
		prevstates.add(universe_tuple)
		# gravity
		for j in range(len(l)):
			for k in range(j + 1, len(l)):
				gravity(l[j], l[k])
		# velocity
		for m in l:
			for i in range(3):
				m[1][i] += m[2][i]
		steps_taken += 1
	return steps_taken

l = new_universe()

for i in range(1000):
	# gravity
	for j in range(len(l)):
		for k in range(j + 1, len(l)):
			gravity(l[j], l[k])
	# velocity
	for m in l:
		for i in range(3):
			m[1][i] += m[2][i]

e = sum([total_energy(m) for m in l])
print("Part 1")
print(e)

x_steps = steps_till_index_repeats(0)
y_steps = steps_till_index_repeats(1)
z_steps = steps_till_index_repeats(2)

print("Part 2")
print(lcm(lcm(x_steps, y_steps), z_steps))