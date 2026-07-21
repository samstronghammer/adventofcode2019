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

def c_to_i(c):
  return ord(c)

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

c = intcode.Computer(get_input(instr))
while True:
  val = c.calc()
  if c.halted:
    break
  if val > 256:
    print("Part 1")
    print(val)
  elif debug_mode:
    print(i_to_c(val), end="")
  

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

c2 = intcode.Computer(get_input(instr2))
while True:
  val = c2.calc()
  if c2.halted:
    break
  if val > 256:
    print("Part 2")
    print(val)
    break
  elif debug_mode:
    print(i_to_c(val), end="")