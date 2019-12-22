#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import intcode
import math

inputx = 0
inputy = 0
sending_x = True

def get_input(x, y):
	yield x
	yield y

locs = {}
tot_pulled = 0
for x in range(0, 50):
	for y in range(0, 50):
		c = intcode.Computer(get_input(x, y))
		pulled = c.calc()
		locs[(x, y)] = pulled
		if pulled == 1:
			tot_pulled += 1

print("Part 1")
print(tot_pulled)

start = (7, 9)
curr_bott = start
curr_top = start
botts = []
tops = set()

for i in range(2000):
	botts.append(curr_bott)
	tops.add(curr_top)
	c_bott = intcode.Computer(get_input(curr_bott[0], curr_bott[1] + 1))
	if c_bott.calc() == 1:
		curr_bott = (curr_bott[0], curr_bott[1] + 1)
	else:
		curr_bott = (curr_bott[0] + 1, curr_bott[1])
	c_top = intcode.Computer(get_input(curr_top[0] + 1, curr_top[1]))
	if c_top.calc() == 1:
		curr_top = (curr_top[0] + 1, curr_top[1])
	else:
		curr_top = (curr_top[0], curr_top[1] + 1)

ans = None
i = 0
square_size = 100
while ans == None:
	if util.vecadd((square_size - 1, 1 - square_size), botts[i]) in tops:
		ans = util.vecadd((0, 1 - square_size), botts[i])
	else:
		i += 1

print("Part 2")
print(ans[0] * 10000 + ans[1])