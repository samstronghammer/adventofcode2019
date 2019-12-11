#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import math
from enum import Enum, unique

# Not the cleanest solution (I copy pasted some code to get part 1
# and part 2 printing properly), but I didn't really struggle with
# bugs today. Everything went well. My main issue is that my
# intcode computer isn't really designed to be interactive yet.
# I need to make some changes to the base computer so future
# intcode problems are faster.

@unique
class DIR(Enum):
    UP = 0
    RIGHT = 1
    LEFT = 2
    DOWN = 3

def get_left(d):
	if d == DIR.UP:
		return DIR.LEFT
	if d == DIR.LEFT:
		return DIR.DOWN
	if d == DIR.DOWN:
		return DIR.RIGHT
	if d == DIR.RIGHT:
		return DIR.UP
	assert(False)

def get_right(d):
	if d == DIR.UP:
		return DIR.RIGHT
	if d == DIR.LEFT:
		return DIR.UP
	if d == DIR.DOWN:
		return DIR.LEFT
	if d == DIR.RIGHT:
		return DIR.DOWN
	assert(False)

def get_move(loc, d):
	if d == DIR.UP:
		return util.vecadd(loc, (0, -1))
	if d == DIR.LEFT:
		return util.vecadd(loc, (-1, 0))
	if d == DIR.DOWN:
		return util.vecadd(loc, (0, 1))
	if d == DIR.RIGHT:
		return util.vecadd(loc, (1, 0))
	assert(False)

def getval(opcodes, relbase, index, mode):
	if mode == "0":
		if not opcodes[index] in opcodes:
			opcodes[opcodes[index]] = 0
		return opcodes[opcodes[index]]
	elif mode == "1":
		return opcodes[index]
	elif mode == "2":
		if not (opcodes[index] + relbase) in opcodes:
			opcodes[opcodes[index] + relbase] = 0
		return opcodes[opcodes[index] + relbase]
	else:
		assert(False)

def calc_with_input(input_vals, opcodes, i, relbase):
	outputs = []
	while True:
		nakedstr = str(opcodes[i])
		letters = "0" * (5 - len(nakedstr)) + str(opcodes[i])
		code = int("".join(letters[3:]))
		if code > 0 and code < 10:
			if code == 1 or code == 2:
				a1 = getval(opcodes, relbase, i + 1, letters[2])
				a2 = getval(opcodes, relbase, i + 2, letters[1])
				loc = opcodes[i + 3] + (relbase if letters[0] == "2" else 0)
				sol = a1 + a2 if code == 1 else a1 * a2
				opcodes[loc] = sol
				i += 4
			if code == 3:
				if len(input_vals) == 0:
					return False, outputs, (opcodes, i, relbase)
				input_val = input_vals.pop(0)
				if letters[2] == "2":
					opcodes[opcodes[i + 1] + relbase] = input_val
				else:
					opcodes[opcodes[i + 1]] = input_val
				i += 2
			if code == 4:
				ans = getval(opcodes, relbase, i + 1, letters[2])
				i += 2
				outputs.append(ans)
			if code == 5 or code == 6:
				a1 = getval(opcodes, relbase, i + 1, letters[2])
				a2 = getval(opcodes, relbase, i + 2, letters[1])
				if (a1 != 0 and code == 5) or (a1 == 0 and code == 6):
					i = a2
				else:
					i += 3
			if code == 7 or code == 8:
				a1 = getval(opcodes, relbase, i + 1, letters[2])
				a2 = getval(opcodes, relbase, i + 2, letters[1])
				loc = opcodes[i + 3] + (relbase if letters[0] == "2" else 0)
				if (a1 < a2 and code == 7) or (a1 == a2 and code == 8):
					opcodes[loc] = 1
				else:
					opcodes[loc] = 0
				i += 4
			if code == 9:
				relbase = relbase + getval(opcodes, relbase, i + 1, letters[2])
				i += 2
		elif code == 99:
			return True, outputs, (opcodes, i, relbase)
			break
		else:
			print("ERROR")
			print(code)
			return

fn = "./in.txt"
l = util.filetowordlist("./in.txt")
b = list(map(lambda x: int(x), l[0].split(",")))
state = {}
for q in range(len(b)):
	state[q] = b[q]
c = (state, 0, 0)
panels = {}
loc = (0, 0)
direction = DIR.UP

while True:
	if not loc in panels:
		panels[loc] = 0
	done, outputs, vals = calc_with_input([panels[loc]], c[0], c[1], c[2])
	c = vals
	panels[loc] = outputs[0]
	if outputs[1] == 0:
		direction = get_left(direction)
	else:
		direction = get_right(direction)
	loc = get_move(loc, direction)
	if done:
		break

util.clear_terminal()
util.print_at_loc((1, 1), "Part 1")
util.print_at_loc((1, 2), len(panels))

state = {}
for q in range(len(b)):
	state[q] = b[q]
c = (state, 0, 0)
panels = {}
panels[(0, 0)] = 1
loc = (0, 0)
direction = DIR.UP

while True:
	if not loc in panels:
		panels[loc] = 0
	done, outputs, vals = calc_with_input([panels[loc]], c[0], c[1], c[2])
	c = vals
	panels[loc] = outputs[0]
	if outputs[1] == 0:
		direction = get_left(direction)
	else:
		direction = get_right(direction)
	loc = get_move(loc, direction)
	if done:
		break

util.print_at_loc((1, 3), "Part 2")
for key in panels:
	char = "." if panels[key] == 0 else "#"
	util.print_at_loc(util.vecadd(key, (1, 4)), char)
print("")