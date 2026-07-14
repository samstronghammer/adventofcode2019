#!/usr/bin/python3
import sys
sys.path.append("..")
import intcode

# Non-graphical solution. I think today was very interesting!
# It's amazing to me that the input file is the brain of an
# entire game.

def get_input_list(l):
  for x in l:
    yield x

c = intcode.Computer()
panels = {}

paddle_x = 0
ball_x = 0

output = c.calc_list()
for i in range(len(output)//3):
  s = i * 3
  panels[(output[s], output[s + 1])] = output[s + 2]
  if output[s+2] == 4:
    ball_x = output[s]
  if output[s+2] == 3:
    paddle_x = output[s]

print("Part 1")
tot = 0
for k in panels:
  if panels[k] == 2:
    tot += 1
print(tot)

c = intcode.Computer()
c.write(0, 2)

score = 0
while True:
  joystick = -1 if ball_x < paddle_x else (1 if ball_x > paddle_x else 0)
  c.get_input = get_input_list([joystick])
  outputs = c.calc_list()
  for i in range(len(outputs)//3):
    s = i * 3
    if outputs[s+2] == 4:
      ball_x = outputs[s]
    if outputs[s+2] == 3:
      paddle_x = outputs[s]
    if outputs[s] == -1 and outputs[s+1] == 0:
      score = outputs[s+2]
    else:
      panels[(outputs[s], outputs[s + 1])] = outputs[s + 2]
  if c.halted:
    break
print("Part 2")
print(score)


