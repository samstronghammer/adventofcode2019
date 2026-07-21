#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import intcode 

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

graphical = False # change this to turn the livefeed on/off

def draw_game(panels, offset):
  if not graphical:
    return
  for key in panels:
    util.print_at_loc(util.vecadd(key, offset), panels[key])

comp = intcode.Computer()

a = {}
r = 0
c = 0
start_pos = None
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
    if char in ["^", "<", "v", ">"]:
      start_pos = (c, r)
    c += 1

# Part 1 calculation
tot = 0
for k in a:
  if a[k] != "#":
    continue
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

util.clear_terminal()

util.print_at_loc((1, 1), "Part 1")
util.print_at_loc((1, 2), tot)
util.print_at_loc((1, 3), "Part 2")


def robot_to_direction(c):
  match c:
    case "^":
      return (0, -1)
    case "<":
      return (-1, 0)
    case "v":
      return (0, 1)
    case ">":
      return (1, 0)


# Calculates an instruction path using the structure of the input
def calc_instructions(start_pos, panels):
  curr_dir = robot_to_direction(panels[start_pos])
  curr_pos = start_pos
  instructions = []
  while True:
    # try straight
    straight_pos = util.vecadd(curr_pos, curr_dir)
    straight_char = panels.get(straight_pos, ".")
    if straight_char == "#":
      curr_pos = straight_pos
      instructions[-1] += 1
      continue
    # try left 
    left_dir = util.col_row_dir_turn_left(curr_dir)
    left_pos = util.vecadd(curr_pos, left_dir)
    left_char = panels.get(left_pos, ".")
    if left_char == "#":
      curr_dir = left_dir
      curr_pos = left_pos
      instructions.append("L")
      instructions.append(1)
      continue
    # try right 
    right_dir = util.col_row_dir_turn_right(curr_dir)
    right_pos = util.vecadd(curr_pos, right_dir)
    right_char = panels.get(right_pos, ".")
    if right_char == "#":
      curr_dir = right_dir
      curr_pos = right_pos
      instructions.append("R")
      instructions.append(1)
      continue
    # dead end, done
    return [str(x) for x in instructions]

all_instructions = calc_instructions(start_pos, a)
all_subroutine_chars = ["A", "B", "C"]

# Replace a subroutine in an instruction list
def replace(instructions, subroutine_char, subroutine_instructions):
  curr_instructions = instructions[:]
  curr_index = 0
  while curr_index < len(curr_instructions):
    for offset in range(len(subroutine_instructions)):
      subroutine_instruction = subroutine_instructions[offset]
      if curr_index + offset >= len(curr_instructions):
        break
      main_instruction = curr_instructions[curr_index + offset]
      if subroutine_instruction != main_instruction:
        break
    else:
      curr_instructions = curr_instructions[0:curr_index] + [subroutine_char] + curr_instructions[curr_index + len(subroutine_instructions):]
    curr_index += 1
  return curr_instructions

def is_done(instructions):
  return all(map(lambda x: x in all_subroutine_chars, instructions))

# Takes in instructions, returns dict mapping chars to instruction lists or none if invalid
def find_subroutines(instructions, subroutine_chars_left):
  if len(subroutine_chars_left) == 0:
    if is_done(instructions):
      return dict()
    return None

  subroutine_char = subroutine_chars_left[0]
  remaining_subroutine_chars = subroutine_chars_left[1:]
  start_index = list(map(lambda x: x in all_subroutine_chars, instructions)).index(False) # find first index after subroutine instructions
  for end_index in range(start_index, len(instructions)):
    subroutine_instructions = instructions[start_index:end_index + 1]
    if any(map(lambda x: x in subroutine_chars_left, subroutine_instructions)):
      break 
    subroutine_length = len(",".join(subroutine_instructions))
    if subroutine_length > 20: # too long
      break
    replaced_instructions = replace(instructions, subroutine_char, subroutine_instructions)
    recursive_result = find_subroutines(replaced_instructions, remaining_subroutine_chars)
    if recursive_result == None:
      continue
    recursive_result[subroutine_char] = subroutine_instructions
    return recursive_result 

  return None

subroutines = find_subroutines(all_instructions, all_subroutine_chars) # {routine char: subroutine instruction list}
main_instructions = all_instructions
for c in all_subroutine_chars:
  main_instructions = replace(main_instructions, c, subroutines[c])
routines = [main_instructions, *(subroutines[x] for x in all_subroutine_chars), ["y" if graphical else "n"]]
total = "\n".join([",".join(x) for x in routines]) + "\n"
input_index = 0

def get_input_func2():
  for instruction in total:
    yield ord(instruction)

comp2 = intcode.Computer(get_input_func2())
comp2.write(0, 2)
a = {}
r = 0
c = 0
just_added_row = False
while True:
  val = comp2.calc()
  if val == None:
    break
  if val > 256:
    util.print_at_loc((1, 4), val)
    break
  else:
    if val == 10:
      if just_added_row:
        draw_game(a, (1, 5))
        a = {}
        r = 0
        c = 0
      else:
        r += 1
        c = 0
        just_added_row = True
    else:
      just_added_row = False
      char = str(chr(val))
      a[(c, r)] = char
      c += 1
if graphical:
  util.print_at_loc((1, 70), "")

