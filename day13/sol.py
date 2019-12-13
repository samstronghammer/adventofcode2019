#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import math
from enum import Enum, unique
import time

# Non-graphical solution. I think today was very interesting!
# It's amazing to me that the input file is the brain of an
# entire game.

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
state[0] = 2
c = (state, 0, 0)
panels = {}

paddle_x = 0
ball_x = 0

while True:
	done, outputs, vals = calc_with_input([], c[0], c[1], c[2])
	for i in range(len(outputs)//3):
		s = i * 3
		panels[(outputs[s], outputs[s + 1])] = outputs[s + 2]
		if outputs[s+2] == 4:
			ball_x = outputs[s]
		if outputs[s+2] == 3:
			paddle_x = outputs[s]
	break

print("Part 1")
tot = 0
for k in panels:
	if panels[k] == 2:
		tot += 1
print(tot)

score = 0
while True:
	joystick = -1 if ball_x < paddle_x else (1 if ball_x > paddle_x else 0)
	done, outputs, vals = calc_with_input([joystick], c[0], c[1], c[2])
	c = vals
	for i in range(len(outputs)//3):
		s = i * 3
		if outputs[s+2] == 4:
			ball_x = outputs[s]
		if outputs[s+2] == 3:
			paddle_x = outputs[s]
		if outputs[s] == -1 and outputs[s+1] == 0:
			score = outputs[s+2]
		else:
			panels[(outputs[s], outputs[s + 1])] = outputs[s + 2]
	if done:
		break
print("Part 2")
print(score)


