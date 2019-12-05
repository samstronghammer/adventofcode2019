#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import math

# Ugh. This was tough to push through. Very easy to write bugs.
# Am planning on writing a better intcode computer.

fn = "./in.txt"
l = util.filetowordlist("./in.txt")

def calc_with_input(input_val):
	opcodes = list(map(lambda x: int(x), l[0].split(",")))
	i = 0
	while True:
		nakedstr = str(opcodes[i])
		letters = "0" * (5 - len(nakedstr)) + str(opcodes[i])
		code = int("".join(letters[3:]))
		par1imm = letters[2] == "1"
		par2imm = letters[1] == "1"
		par3imm = letters[0] == "1"
		if code > 0 and code < 9:
			if code == 1 or code == 2:
				a1 = opcodes[i + 1] if par1imm else opcodes[opcodes[i + 1]]
				a2 = opcodes[i + 2] if par2imm else opcodes[opcodes[i + 2]]
				loc = opcodes[i + 3]
				sol = a1 + a2 if code == 1 else a1 * a2
				opcodes[loc] = sol
				i += 4
			if code == 3:
				opcodes[opcodes[i + 1]] = input_val
				i += 2
			if code == 4:
				ans = opcodes[i + 1] if par1imm else opcodes[opcodes[i + 1]]
				print("output: " + str(ans))
				i += 2
			if code == 5 or code == 6:
				a1 = opcodes[i + 1] if par1imm else opcodes[opcodes[i + 1]]
				a2 = opcodes[i + 2] if par2imm else opcodes[opcodes[i + 2]]
				if (a1 != 0 and code == 5) or (a1 == 0 and code == 6):
					i = a2
				else:
					i += 3
			if code == 7 or code == 8:
				a1 = opcodes[i + 1] if par1imm else opcodes[opcodes[i + 1]]
				a2 = opcodes[i + 2] if par2imm else opcodes[opcodes[i + 2]]
				loc = opcodes[i + 3]
				if (a1 < a2 and code == 7) or (a1 == a2 and code == 8):
					opcodes[loc] = 1
				else:
					opcodes[loc] = 0
				i += 4
		elif code == 99:
			break
		else:
			print("ERROR")
			print(code)
			return

print("Part 1")
calc_with_input(1)
print("Part 2")
calc_with_input(5)