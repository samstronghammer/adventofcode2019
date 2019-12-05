#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import math
l = util.filetowordlist("./in.txt")
for n in range(100):
	for v in range(100):
		opcodes = list(map(lambda x: int(x), l[0].split(",")))
		opcodes[1] = n
		opcodes[2] = v
		i = 0
		while True:
			code = opcodes[i]
			if code == 1 or code == 2:
				a1 = opcodes[opcodes[i + 1]]
				a2 = opcodes[opcodes[i + 2]]
				loc = opcodes[i + 3]
				sol = a1 + a2 if code == 1 else a1 * a2
				opcodes[loc] = sol
			elif code == 99:
				break
			else:
				print("ERROR")
				print(code)
				break
			i += 4
		if n == 12 and v == 2:
			print("Part 1")
			print(opcodes[0])
		if opcodes[0] == 19690720:
			print("Part 2")
			print(100 * n + v)
