#!/usr/bin/python3
import sys
sys.path.append("..")
import util
from enum import Enum, unique
import intcode

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

panels = {}
loc = (0, 0)
direction = DIR.UP
def get_input(loc):
  yield panels[loc]

c = intcode.Computer()

while True:
  if not loc in panels:
    panels[loc] = 0
  c.get_input = get_input(loc)
  output = []
  while True:
    one_output = c.calc()
    if one_output == None:
      break
    output.append(one_output)

  panels[loc] = output[0]
  if output[1] == 0:
    direction = get_left(direction)
  else:
    direction = get_right(direction)
  loc = get_move(loc, direction)
  if c.halted:
    break

util.clear_terminal()
util.print_at_loc((1, 1), "Part 1")
util.print_at_loc((1, 2), len(panels))

panels = {}
panels[(0, 0)] = 1
loc = (0, 0)
direction = DIR.UP

def get_input(loc):
  yield panels[loc]

c = intcode.Computer()

while True:
  if not loc in panels:
    panels[loc] = 0
  c.get_input = get_input(loc)
  output = []
  while True:
    one_output = c.calc()
    if one_output == None:
      break
    output.append(one_output) 

  panels[loc] = output[0]
  if output[1] == 0:
    direction = get_left(direction)
  else:
    direction = get_right(direction)
  loc = get_move(loc, direction)
  if c.halted:
    break

util.print_at_loc((1, 3), "Part 2")
for key in panels:
  char = " " if panels[key] == 0 else "#"
  util.print_at_loc(util.vecadd(key, (1, 4)), char)
print("")