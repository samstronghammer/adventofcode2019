#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import math

# Oof, this didn't go well. I don't perform well under time pressure with trees.
# About halfway through I realized that this method was very inefficient
# and totally unnecessary. The (parent, child) pairing threw me off-- my first
# thought *should* have been a hash map. Ah well, my worst night so far. Almost
# went over 1000th. Check out the redemption_sol.py for my second (much cleaner)
# attempt.

class Tree:
	def __init__(self, root_name):
		self.root_name = root_name
		self.children = {}

	def insert(self, parent_name, name):
		if self.root_name == parent_name:
			self.children[name] = Tree(name)
			return True
		else:
			for c in self.children:
				if self.children[c].insert(parent_name, name):
					return True
		return False

	def num_orbits(self, acc):
		tot = 0
		# for self
		tot += acc
		# for children
		for c in self.children:
			tot += self.children[c].num_orbits(acc + 1)

		return tot

fn = "./in.txt"

l = [(x.split(")")[0], x.split(")")[1]) for x in util.filetowordlist(fn)]

t = Tree("COM")

while len(l) > 0:
	print(len(l))
	notdone = []
	for p in l:
		if not t.insert(p[0], p[1]):
			notdone.append(p)
	l = notdone

linetoyou = []
linetosanta = []
child_parent_map = {}
for p in [(x.split(")")[0], x.split(")")[1]) for x in util.filetowordlist(fn)]:
	child_parent_map[p[1]] = p[0]

curr = child_parent_map["YOU"]
while curr != "COM":
	linetoyou.append(curr)
	curr = child_parent_map[curr]
curr = child_parent_map["SAN"]
while curr != "COM":
	linetosanta.append(curr)
	curr = child_parent_map[curr]

ans = -1
for star in linetoyou:
	if star in linetosanta:
		print(linetoyou.index(star))
		print(linetosanta.index(star))
		ans = linetoyou.index(star) + linetosanta.index(star)
		break


print("Part 1")
print(t.num_orbits(0))
print("Part 2")
print(ans)





