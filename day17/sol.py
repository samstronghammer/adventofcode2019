#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import math

# Today was fun! My only complaint was that my robot fell off of the edge of the
# map so I couldn't see where it was and thought the system had glitched or
# something. It also wasn't exactly clear how the "prompting" or "live feed" 
# would work. I figured out that each "frame" of the feed was separated by
# an extra newline, which allowed me to polish the graphical solution.
# My method for writing the movement functions was to write down the entire
# sequence needed and figure out the common chunks. Fairly straightforward.
# I had a dumb bug where I accidentally flipped my r and c values so the entire
# map was flipped. I had to switch all of the Ls to Rs and vice versa.
# Part 1 of today was my best placement so far this year! 126th :)

class Computer():
	def __init__(self, get_input=lambda: None, filename="in.txt", i=0, relbase=0):
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
					# print(f"HI: {input_val}")
					if input_val == None:
						# print("NONE")
						return None
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

comp = Computer()

a = {}
r = 0
c = 0
while True:
	val = comp.calc()
	if val == None:
		break
	if val == 10:
		r += 1
		c = 0
	else:
		char = str(chr(val))
		a[(c, r)] = char
		c += 1

tot = 0
for k in a:
	intersection = True
	for adj in util.adj4(k):
		if not adj in a:
			intersection = False
			break
		if a[adj] == ".":
			intersection = False
			break
	if intersection:
		tot += k[0]*k[1]

print("Part 1")
print(tot)
print("Part 2")

A = "L,12,L,12,R,12"
B = "L,8,L,8,R,12,L,8,L,8"
C = "L,10,R,8,R,12"
master = "A,A,B,C,C,A,B,C,A,B"

total = master + "\n" + A + "\n" + B + "\n" + C + "\n" + "n" + "\n"
input_index = 0

def get_input_func2():
	global input_index
	ans = ord(total[input_index])
	input_index += 1
	return ans

comp2 = Computer(get_input=get_input_func2)
comp2.write(0, 2)
while True:
	val = comp2.calc()
	if val == None:
		break
	if val > 256:
		print(val)

