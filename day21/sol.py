#!/usr/bin/python3
import sys
sys.path.append("..")
import intcode

# Interesting puzzle. I found the small number of mutable registers
# to be very limiting. Once I figured out that "or"ing together the
# three spots in front could be done in one register things fell
# into place.

debug_mode = False 

def i_to_c(i):
  return str(chr(i))

def get_input(s):
  for c in s:
    yield ord(c)

instr="""OR A J
AND B J
AND C J
NOT J J
AND D J
WALK
"""

vals = intcode.Computer(get_input(instr)).calc_list()
ans = None
for val in vals:
  if val > 256:
    ans = val
    break
  elif debug_mode:
    print(i_to_c(val), end="")
print("Part 1")
print(ans)
  

instr2="""OR E T
OR H T
OR A J
AND B J
AND C J
NOT J J
AND T J
AND D J
RUN
"""

vals = intcode.Computer(get_input(instr2)).calc_list()
for val in vals:
  if val > 256:
    ans = val
    break
  elif debug_mode:
    print(i_to_c(val), end="")
print("Part 2")
print(ans)