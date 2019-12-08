#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import math

# Solving the feeding into each other problem was interesting-- my first
# thought was how threads in Golang talk to each other and use channels.
# Wasn't an option here though, so I just fed as much input as possible into
# each computer, and took its output and fed it into the next computer.
# I got stuck and was tired, so I went to bed and didn't finish. Found my
# bug the next day-- I'd initialized the computer array in the wrong place.

fn = "./in.txt"
l = util.filetowordlist("./in.txt")

def calc_with_input(list_inputs, state, currindex):
	liindex = 0
	opcodes = state
	i = currindex
	outputs = []
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
				if liindex >= len(list_inputs):
					return ((opcodes, i), outputs, False)
				opcodes[opcodes[i + 1]] = list_inputs[liindex]
				liindex += 1
				i += 2
			if code == 4:
				ans = opcodes[i + 1] if par1imm else opcodes[opcodes[i + 1]]
				outputs.append(ans)
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
			return ((opcodes, i), outputs, True)
			break
		else:
			print("ERROR")
			print(code)
			return

def get_perm(acc, left):
	if len(left) == 0:
		return [acc]
	retval = []
	for i in range(0, len(left)):
		t = left[i]
		retval += get_perm((acc + [t]).copy(), left[0:i] + left[i+1:])
	return retval

inlist = list(map(lambda x: int(x), l[0].split(",")))

lilists = get_perm([], [0, 1, 2, 3, 4])
best_output = 0
best_phases = []
for l2 in lilists:
	cinput = 0
	for p in l2:
		computer = (inlist.copy(), 0, False)
		_, output, _ = calc_with_input([p, cinput], computer[0], computer[1])
		output = output[0]
		cinput = output
	if output > best_output:
		best_output = output
		best_phases = l2
print("Part 1")
print(best_output)

lilists2 = get_perm([], [5, 6, 7, 8, 9])
best_output2 = 0
best_phases2 = []
for l2 in lilists2:
	computers = [(inlist.copy(), 0, False) for x in range(0, 5)]
	cinput = [0]
	output = 0
	first_time = True
	while True:
		for i in range(len(l2)):
			if first_time:
				cinput = [l2[i]] + cinput
			c = computers[i]
			if c[2]:
				not_finished = False
				break
			state, outputstuff, finished = calc_with_input(cinput, c[0], c[1])
			computers[i] = (state[0], state[1], finished)
			cinput = outputstuff
		else: 
			first_time = False
			continue
		break
	fin_output = cinput[-1]
	if fin_output > best_output2:
		best_output2 = fin_output
		best_phases2 = l2
print("Part 2")
print(best_output2)
