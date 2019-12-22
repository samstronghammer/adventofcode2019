#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import math
from enum import unique, Enum
import time

# Change the tic speeds set here to see how the maze construction
# and oxygen algorithms work.
maze_tic_speed = 0
oxygen_tic_speed = 0
# I improved the drawing of the maze to be almost instant.

@unique
class DIR(Enum):
    UP = 1
    RIGHT = 4
    LEFT = 3
    DOWN = 2

def get_back(d):
	if d == DIR.UP:
		return DIR.DOWN
	if d == DIR.LEFT:
		return DIR.RIGHT
	if d == DIR.DOWN:
		return DIR.UP
	if d == DIR.RIGHT:
		return DIR.LEFT
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

class Computer():
	def __init__(self, filename="in.txt", i=0, relbase=0):
		l = util.filetointcode(filename)
		self.state = {}
		for q in range(len(l)):
			self.write(q, l[q])
		self.i = i
		self.relbase = relbase
		self.halted = False

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

	def calc(self, input_vals):
		outputs = []
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
					if len(input_vals) == 0:
						return outputs
					input_val = input_vals.pop(0)
					if letters[2] == "2":
						self.write(self.read(self.i + 1) + self.relbase, input_val)
					else:
						self.write(self.read(self.i + 1), input_val)
					self.i += 2
				if code == 4:
					ans = self.getval(self.i + 1, letters[2])
					outputs.append(ans)
					self.i += 2
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
				return outputs
				break
			else:
				print("ERROR")
				print(code)
				return

def get_dir(prev, dest):
	d = {(0, -1): DIR.UP, (0, 1): DIR.DOWN, (1, 0): DIR.RIGHT, (-1, 0): DIR.LEFT}
	return d[util.vecminus(dest, prev)]

def n_to_c(n):
	if n == 0:
		return "."
	if n == 1:
		return "#"
	if n == 2:
		return "!"

def draw_game(new_panel, offset, new_loc, old_loc):
	util.print_at_loc(util.vecadd(old_loc, offset), ".")
	if new_panel != None:
		util.print_at_loc(util.vecadd(new_panel[0], offset), new_panel[1])
	util.print_at_loc(util.vecadd(new_loc, offset), "0")

def draw_maze(panels, offset):
	for p in panels:
		util.print_at_loc(util.vecadd(p, offset), n_to_c(panels[p][0]))

def draw_oxygen(new_oxygen_locs, offset):
	for l in new_oxygen_locs:
		util.print_at_loc(util.vecadd(l, offset), 'o')

def dijkstra(panels):
	source = (0, 0)
	dists = {}
	prevs = {}
	Q = set()
	for p in panels:
		dists[p] = 99999999999
		prevs[p] = None
		Q.add(p)
	dists[source] = 0
	while len(Q) > 0:
		minv = None
		for q in Q:
			if minv == None:
				minv = q
			else:
				if dists[minv] > dists[q]:
					minv = q
		Q.remove(minv)
		for q in util.adj4(minv):
			if q in Q:
				alt = dists[minv] + 1
				if alt < dists[q]:
					dists[q] = alt
	return dists

loc = (0, 0)
c = Computer()
# 0: ok, 1: wall, 2: system
# second part of tuple is list of [completed, backtrack dir]
panels = {(0, 0): (0, [False, None])}
util.clear_terminal()
while not panels[loc][1][0] or panels[loc][1][1] != None:
	# add in this line to watch the logic of the maze construction
	time.sleep(maze_tic_speed)
	old_loc = loc
	new_panel = None
	if panels[loc][1][0]:
		# backtrack
		_, = c.calc([panels[loc][1][1].value])
		loc = get_move(loc, panels[loc][1][1])
	else:
		# explore
		next_place = None
		for new_place in util.adj4(loc):
			if not new_place in panels:
				next_place = new_place
				break
		if next_place == None:
			panels[loc][1][0] = True
		else:
			step = get_dir(loc, next_place)
			out, = c.calc([step.value])
			if out == 0:
				panels[next_place] = (1, [True, get_back(step)])
				new_panel = (next_place, "#")
			else:
				loc = next_place
				panels[loc] = (0, [False, get_back(step)]) if out == 1 else (2, [False, get_back(step)])
				new_panel = (loc, "." if out == 1 else "!")
	draw_game(new_panel, (22, 22), loc, old_loc)

filtered_panels = {}
oxygen_loc = None
for loc in panels:
	if panels[loc][0] != 1:
		filtered_panels[loc] = panels[loc][0]
	if panels[loc][0] == 2:
		oxygen_loc = loc
util.print_at_loc((1, 42), "Part 1")
util.print_at_loc((1, 43), dijkstra(filtered_panels)[oxygen_loc])
util.print_at_loc((1, 44), "Press Enter To Continue")
input()
util.clear_terminal()
draw_maze(panels, (22,22))
oxygen = set()
oxygen.add(oxygen_loc)
no_oxygen = set()
for p in filtered_panels:
	no_oxygen.add(p)
no_oxygen.remove(oxygen_loc)
draw_oxygen(oxygen, (22,22))
mins = 0
while len(no_oxygen) > 0:
	time.sleep(oxygen_tic_speed)
	possible_new = set()
	for o in oxygen:
		for n in util.adj4(o):
			possible_new.add(n)
	actual_new = no_oxygen.intersection(possible_new)
	for o in actual_new:
		no_oxygen.remove(o)
		oxygen.add(o)
	draw_oxygen(actual_new, (22,22))
	mins += 1
util.print_at_loc((1, 42), "Part 2")
util.print_at_loc((1, 43), mins)
