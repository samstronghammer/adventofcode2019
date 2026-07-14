#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import math
import intcode
l = util.filetowordlist("./in.txt")

def calc_ans(input):
  c = intcode.Computer()
  c.write(1, input[0])
  c.write(2, input[1])
  c.calc()
  return c.read(0)

def calc_p2():
  bigger = 0
  ans = None
  while True:
    for smaller in range(bigger + 1):
      ans1 = calc_ans((bigger, smaller))
      if ans1 == 19690720:
        ans = (bigger, smaller)
      ans2 = calc_ans((smaller, bigger))
      if ans2 == 19690720:
        ans = (smaller, bigger)
    bigger += 1
    if ans != None:
      break
  return 100 * ans[0] + ans[1]

print("Part 1:")
print(calc_ans((12, 2)))
print("Part 2:")
print(calc_p2())
