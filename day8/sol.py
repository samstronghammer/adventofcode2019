#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import math

# 12:16 -> start
# 12:26 -> part 1
# 12:32 -> part 2
# Accidentally started late today. Still wouldn't have made it on the leaderboard
# though, ah well. Cool challenge! I liked working with the indices. For a hot second
# I didn't see the message encoded in the 1s and 0s and got scared.

fn = "./in.txt"

digits = [int(x) for x in util.filetocleancharlist(fn)]
layers = []
w = 25
h = 6
sz = w * h
k = 0
while k < len(digits):
	layers.append(digits[k:k+sz])
	k += sz

fz = layers[0]
fzcount = layers[0].count(0)
for l in layers:
	if l.count(0) < fzcount:
		fz = l
		fzcount = l.count(0)
print("Part 1")
print(fz.count(1) * fz.count(2))

ans = []
for i in range(sz):
	pl = []
	for l in layers:
		pl.append(l[i])
	color = 2
	for p in pl:
		if p == 0:
			color = 0
			break
		if p == 1:
			color = 1
			break
	ans.append(color)

print("Part 2")
for i in range(h):
	print("".join([str(x) for x in ans[i * w:(i+1) * w]]))




