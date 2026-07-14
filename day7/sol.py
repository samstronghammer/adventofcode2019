#!/usr/bin/python3
import sys
sys.path.append("..")
import intcode

# Solving the feeding into each other problem was interesting-- my first
# thought was how threads in Golang talk to each other and use channels.
# Wasn't an option here though, so I just fed as much input as possible into
# each computer, and took its output and fed it into the next computer.
# I got stuck and was tired, so I went to bed and didn't finish. Found my
# bug the next day-- I'd initialized the computer array in the wrong place.

def get_perm(acc, left):
  if len(left) == 0:
    return [acc]
  retval = []
  for i in range(0, len(left)):
    t = left[i]
    retval += get_perm((acc + [t]).copy(), left[0:i] + left[i+1:])
  return retval

def get_input_from_list(l):
  for x in l:
    yield x

lilists = get_perm([], [0, 1, 2, 3, 4])
best_output = 0
best_phases = []
for l2 in lilists:
  cinput = 0
  for p in l2:
    c = intcode.Computer(get_input_from_list([p, cinput]))
    output = c.calc()
    cinput = output
  if output > best_output:
    best_output = output
    best_phases = l2
print("Part 1")
print(best_output)

lilists2 = get_perm([], [5, 6, 7, 8, 9])
best_output2 = 0
best_phases2 = []
for l2 in lilists2:
  computers = [intcode.Computer() for x in range(0, 5)]
  cinput = [0]
  output = 0
  first_time = True
  while True:
    for i in range(len(l2)):
      if first_time:
        cinput = [l2[i]] + cinput
      c = computers[i]
      if c.halted:
        break
      c.get_input = get_input_from_list(cinput)
      raw_output = c.calc()
      if i == len(l2) - 1 and raw_output != None:
        output = raw_output
      cinput = [] if raw_output == None else [raw_output]
    else: 
      first_time = False
      continue
    break
  fin_output = output
  if fin_output > best_output2:
    best_output2 = fin_output
    best_phases2 = l2
print("Part 2")
print(best_output2)
