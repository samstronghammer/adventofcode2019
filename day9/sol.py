#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import math

# Sooooo many intcode problems! If I'd known there'd be so many steps I 
# would have spent some time cleaning up the code. Today I had trouble
# finding all the places that the spec stated that relbase comes into
# play. Specifically with the "loc" variables.

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

fn = "./in.txt"
l = util.filetowordlist("./in.txt")

def calc_with_input(input_val):
	b = list(map(lambda x: int(x), l[0].split(",")))
	opcodes = {}
	for q in range(len(b)):
		opcodes[q] = b[q]
	i = 0
	relbase = 0
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
				if letters[2] == "2":
					opcodes[opcodes[i + 1] + relbase] = input_val
				else:
					opcodes[opcodes[i + 1]] = input_val
				i += 2
			if code == 4:
				ans = getval(opcodes, relbase, i + 1, letters[2])
				print("output: " + str(ans))
				i += 2
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
			break
		else:
			print("ERROR")
			print(code)
			return

print("Part 1")
calc_with_input(1)
print("Part 2")
calc_with_input(2)