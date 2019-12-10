#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import math

# I felt like I quickly understood the problem and knew how to solve it,
# but then had issues with small, hard-to-find bugs. A missing pair of 
# parens in part 1 cost me about 10 minutes. Perfecting the angle
# function in part 2 took me longer than it should have. Cool challenge!

def visible(xs, ys, xe, ye, l):
	dy = ye - ys
	dx = xe - xs
	if dy == 0:
		seen = True
		for x2 in range(min(xe, xs) + 1, max(xe, xs)):
			if l[ye][x2] == ".":
				continue
			else:
				return False
		if seen:
			return True
	else:
		if dx == 0:
			seen = True
			for y2 in range(min(ye, ys) + 1, max(ye, ys)):
				if l[y2][xe] == ".":
					continue
				else:
					return False
			if seen:
				return True
		else:
			seen = True
			pstart = (xe, ye) if xe < xs else (xs, ys)
			pend = (xs, ys) if xe < xs else (xe, ye)
			dy2 = pend[1] - pstart[1]
			for x2 in range(pstart[0] + 1, pend[0]):
				y2 = (((x2 - pstart[0]) / abs(dx)) * dy2) + pstart[1]
				if int(y2) != y2:
					continue
				if l[int(y2)][x2] == ".":
					continue
				else:
					return False
			if seen:
				return True
	return False

def astseen(xs, ys, l):
	if l[ys][xs] == ".":
		return 0
	c = 0
	for y in range(len(l)):
		for x in range(len(l[0])):
			if (xs, ys) == (x, y):
				continue
			if l[y][x] == ".":
				continue
			if visible(xs, ys, x, y, l):
				c += 1
	return c

def angle(xs, ys, xe, ye):
	dx = xe - xs
	dy = ys - ye
	theta_radians = math.atan2(dy, dx)
	theta_radians *= -1
	theta_radians += math.pi / 2
	if theta_radians < 0:
		theta_radians += 2 * math.pi
	return theta_radians


fn = "./in.txt"

l = util.filetocleancharlistlist(fn)

bestloc = (0, 0)
bestcount = 0
for y in range(len(l)):
	for x in range(len(l[0])):
		if bestcount < astseen(x, y, l):
			bestcount = astseen(x, y, l)
			bestloc = (x, y)
print("Part 1")
print(bestcount)

center = bestloc
asteroids = {}
for y in range(len(l)):
	for x in range(len(l[0])):
		if l[y][x] == "#":
			theta_radians = angle(center[0], center[1], x, y)
			if not theta_radians in asteroids:
				asteroids[theta_radians] = []
			asteroids[theta_radians].append(((x, y), util.manhattan_dist((x, y), center)))

sorted_keys = sorted(asteroids.keys())
for k in sorted_keys:
	asteroids[k] = sorted(asteroids[k], key=lambda x: x[1])

order_destroyed = []
while len(asteroids.keys()) > 0:
	for k in sorted_keys:
		if k in asteroids:
			ast = asteroids[k].pop()
			if len(asteroids[k]) == 0:
				asteroids.pop(k, None)
			order_destroyed.append(ast)

print("Part 2")
ans = order_destroyed[199][0]
print(ans[0] * 100 + ans[1])



