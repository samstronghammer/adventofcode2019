#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import math

# This works and maintains internal state for me. I think I'll do some
# more cleaning up later.

class Computer():
	def __init__(self, get_input, filename="in.txt", i=0, relbase=0):
		l = util.filetointcode(filename)
		self.state = {}
		for q in range(len(l)):
			self.write(q, l[q])
		self.i = i
		self.relbase = relbase
		self.halted = False
		self.get_input = get_input

	def read(self, index):
		if index in self.state:
			return self.state[index]
		else:
			return 0

	def write(self, index, value):
		self.state[index] = value

	def getval(self, index, mode):
		if mode == "0":
			return self.read(self.read(index))
		elif mode == "1":
			return self.read(index)
		elif mode == "2":
			return self.read(self.read(index) + self.relbase)
		else:
			assert(False)

	def calc(self):
		while True:
			nakedstr = str(self.read(self.i))
			letters = "0" * (5 - len(nakedstr)) + nakedstr
			code = int("".join(letters[3:]))
			if code > 0 and code < 10:
				if code == 1 or code == 2:
					a1 = self.getval(self.i + 1, letters[2])
					a2 = self.getval(self.i + 2, letters[1])
					loc = self.read(self.i + 3) + (self.relbase if letters[0] == "2" else 0)
					sol = a1 + a2 if code == 1 else a1 * a2
					self.write(loc, sol)
					self.i += 4
				if code == 3:
					input_val = self.get_input()
					if letters[2] == "2":
						self.write(self.read(self.i + 1) + self.relbase, input_val)
					else:
						self.write(self.read(self.i + 1), input_val)
					self.i += 2
				if code == 4:
					ans = self.getval(self.i + 1, letters[2])
					self.i += 2
					return ans
				if code == 5 or code == 6:
					a1 = self.getval(self.i + 1, letters[2])
					a2 = self.getval(self.i + 2, letters[1])
					if (a1 != 0 and code == 5) or (a1 == 0 and code == 6):
						self.i = a2
					else:
						self.i += 3
				if code == 7 or code == 8:
					a1 = self.getval(self.i + 1, letters[2])
					a2 = self.getval(self.i + 2, letters[1])
					loc = self.read(self.i + 3) + (self.relbase if letters[0] == "2" else 0)
					if (a1 < a2 and code == 7) or (a1 == a2 and code == 8):
						self.write(loc, 1)
					else:
						self.write(loc, 0)
					self.i += 4
				if code == 9:
					self.relbase = self.relbase + self.getval(self.i + 1, letters[2])
					self.i += 2
			elif code == 99:
				self.halted = True
				return None
			else:
				print("ERROR")
				print(code)
				return None