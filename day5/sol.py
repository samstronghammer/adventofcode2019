#!/usr/bin/python3
import sys
sys.path.append("..")
import intcode

def get_input(x):
	yield x

c = intcode.Computer(get_input(1))
output = 0
while output == 0:
  output = c.calc()
print("Part 1:")
print(output)

c = intcode.Computer(get_input(5))
print("Part 2:")
print(c.calc())
