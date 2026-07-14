#!/usr/bin/python3
import sys
sys.path.append("..")
import util
from enum import unique, Enum
import intcode

# Comment from previous solution:
# My implementation ran pretty slow today. I used pickling to save the panel data after
# finding it once so I never had to redo the calculations. I'm sure there's a much
# better way to explore a maze but this was the best way I could come up with quickly.
# Each panel remembers directions back to the origin. To explore a new spot, the walker
# first goes back to the origin, then to the new location and stores what the new location is.
# I'm considering redoing this later.

# Part two went very quickly. I dropped about 150 places, which was nice.

# Now it's nice and quick.

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

def get_dir(prev, dest):
  d = {(0, -1): DIR.UP, (0, 1): DIR.DOWN, (1, 0): DIR.RIGHT, (-1, 0): DIR.LEFT}
  return d[util.vecminus(dest, prev)]

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
c = intcode.Computer()
# 0: ok, 1: wall, 2: system
# second part of tuple is list of [completed, backtrack dir]
panels = {(0, 0): (0, [False, None])}
while not panels[loc][1][0] or panels[loc][1][1] != None:
  if panels[loc][1][0]:
    # backtrack
    def get_val():
      yield panels[loc][1][1].value
    c.get_input = get_val()
    c.calc()
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
      def get_val():
        yield step.value
      c.get_input = get_val()
      out = c.calc()
      if out == 0:
        panels[next_place] = (1, [True, get_back(step)])
      else:
        loc = next_place
        panels[loc] = (0, [False, get_back(step)]) if out == 1 else (2, [False, get_back(step)])

filtered_panels = {}
oxygen_loc = None
for loc in panels:
  if panels[loc][0] != 1:
    filtered_panels[loc] = panels[loc][0]
  if panels[loc][0] == 2:
    oxygen_loc = loc

print("Part 1")
print(dijkstra(filtered_panels)[oxygen_loc])
print("Part 2")
oxygen = set()
oxygen.add(oxygen_loc)
no_oxygen = set()
for p in filtered_panels:
  no_oxygen.add(p)
no_oxygen.remove(oxygen_loc)

mins = 0
while len(no_oxygen) > 0:
  possible_new = set()
  for o in oxygen:
    for n in util.adj4(o):
      possible_new.add(n)
  actual_new = no_oxygen.intersection(possible_new)
  for o in actual_new:
    no_oxygen.remove(o)
    oxygen.add(o)
  mins += 1
print(mins)
