#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import math

# I was right. Less than half the code and runs lightyears faster.

def find_dist_from_com(name):
	if name in dist_from_com:
		return dist_from_com[name]
	ans = 1 + find_dist_from_com(child_to_parent[name])
	dist_from_com[name] = ans
	return ans

fn = "./in.txt"
l = [(x.split(")")[0], x.split(")")[1]) for x in util.filetowordlist(fn)]
child_to_parent = {}
dist_from_com = {"COM": 0}
for p in l:
	child_to_parent[p[1]] = p[0]
for star in child_to_parent:
	find_dist_from_com(star)

print("Part 1")
print(sum(dist_from_com.values()))

linetoyou = []
linetosanta = []
curr = child_to_parent["YOU"]
while curr != "COM":
	linetoyou.append(curr)
	curr = child_to_parent[curr]
curr = child_to_parent["SAN"]
while curr != "COM":
	linetosanta.append(curr)
	curr = child_to_parent[curr]
for star in linetoyou:
	if star in linetosanta:
		ans = linetoyou.index(star) + linetosanta.index(star)
		break

print("Part 2")
print(ans)