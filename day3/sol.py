#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import math

# I realized after this that a dictionary would have been much faster to type!
def chartovec(c):
	if c == "R":
		return (1, 0)
	elif c == "L":
		return (-1, 0)
	elif c == "U":
		return (0, 1)
	elif c == "D":
		return (0, -1)
	else:
		print("ERROR")
		raise ValueError('bad char')

fn = "./in.txt"
l = util.filetowordlistlist(fn, ",")
locations = {}

for i in range(len(l)):
	wire = l[i]
	currloc = (0, 0)
	dist_to = 0
	for inst in wire:
		d = chartovec(inst[0])
		m = int(inst[1:])
		for j in range(m):
			currloc = util.vecadd(currloc, d)
			dist_to += 1
			if not currloc in locations:
				locations[currloc] = {}
			locations[currloc][i] = dist_to

bestloc = None
bestdist = None
beststeps = None
for key in locations:
	locdict = locations[key]
	if 0 in locdict and 1 in locdict:
		steps = locdict[0] + locdict[1]
		if beststeps == None or steps < beststeps:
			beststeps = steps
	if len(locdict.keys()) == 2 and key != (0,0):
		if bestloc == None or util.manhattan_dist((0, 0), key) < bestdist:
			bestloc = key
			bestdist = util.manhattan_dist((0, 0), key)
print("Part 1")
print(bestdist)
print("Part 2")
print(beststeps)




