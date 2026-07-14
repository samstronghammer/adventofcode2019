#!/usr/bin/python3
import sys
sys.path.append("..")
import intcode

# Sooooo many intcode problems! If I'd known there'd be so many steps I 
# would have spent some time cleaning up the code. Today I had trouble
# finding all the places that the spec stated that relbase comes into
# play. Specifically with the "loc" variables.

def get_input(x):
	yield x

c = intcode.Computer(get_input(1))
print("Part 1:")
print(c.calc())

c = intcode.Computer(get_input(2))
print("Part 2:")
print(c.calc())
