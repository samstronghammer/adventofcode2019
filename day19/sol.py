#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import intcode
import math

# Comment from initial implementation:
# I liked this one. Forces the user to constrain the search space.
# I found the value of 2000 for how far I had to look by guessing
# around. Part 1 went very quickly for me.

# Now it's more robustly able to binary search the search space.

def get_input(x, y):
  yield x
  yield y

def query(loc):
  if loc[0] < 0 or loc[1] < 0:
    return 0
  return intcode.Computer(get_input(loc[0], loc[1])).calc()

locs = {}
for x in range(0, 50):
  for y in range(0, 50):
    locs[(x, y)] = query((x, y))

print("Part 1")
print(sum(locs.values()))

def find_beam_bottom_start():
  y = 49
  while True:
    this_row = [(x, y) for x in range(50)]
    this_row_pulled = [locs[loc] for loc in this_row]
    if sum(this_row_pulled) > 1:
      return this_row[this_row_pulled.index(1)]
    y -= 1

square_size = 100

move_right = (1, 0)
move_left = (-1, 0)

def scan_for_bottom(close_to_bottom):
  val = query(close_to_bottom)
  if val == 0:
    return scan_for_bottom(util.vecadd(close_to_bottom, move_right))
    # move right
  left = query(util.vecadd(close_to_bottom, move_left))
  if left == 0:
    return close_to_bottom
  return scan_for_bottom(util.vecadd(close_to_bottom, move_left))

def calc_top_pulled(bottom):
  top = util.vecadd((square_size - 1, 1 - square_size), bottom)
  return query(top)

min_bottom = find_beam_bottom_start()
max_bottom = scan_for_bottom(util.vecadd(min_bottom, min_bottom))
while True:
  top_pulled = calc_top_pulled(max_bottom)
  if top_pulled == 1:
    break
  min_bottom = max_bottom
  max_bottom = scan_for_bottom(util.vecadd(max_bottom, max_bottom))

def calc_mid_bottom(min_bottom_loc, max_bottom_loc):
  double_loc = util.vecadd(min_bottom_loc, max_bottom_loc)
  close_loc = (math.floor(double_loc[0] / 2), math.floor(double_loc[1] / 2))
  return scan_for_bottom(close_loc)

while True:
  mid_bottom = calc_mid_bottom(min_bottom, max_bottom)
  if mid_bottom == min_bottom or mid_bottom == max_bottom:
    break
  top_pulled = calc_top_pulled(mid_bottom)
  if top_pulled == 1:
    max_bottom = mid_bottom
  else:
    min_bottom = mid_bottom

# Jump back 1% to not miss a rounding problem
curr_bottom = scan_for_bottom(tuple(math.floor(x * 0.99) for x in min_bottom))
while True:
  top_pulled = calc_top_pulled(curr_bottom)
  if top_pulled == 1:
    break
  next_bottom_pulled = intcode.Computer(get_input(curr_bottom[0], curr_bottom[1] + 1)).calc()
  if next_bottom_pulled == 1:
    curr_bottom = (curr_bottom[0], curr_bottom[1] + 1)
  else:
    curr_bottom = (curr_bottom[0] + 1, curr_bottom[1])

ans = util.vecadd((0, 1 - square_size), curr_bottom)
print("Part 2")
print(ans[0] * 10000 + ans[1])
