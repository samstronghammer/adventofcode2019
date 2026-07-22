#!/usr/bin/python3
import sys
sys.path.append("..")
import intcode 

# Did not solve this problem in 2019.
# Required a small tweak to the intcode computer to allow calculation
# one step at a time without blocking.


# id -> remaining inputs
packets = dict()
# id -> partial packet list
partials = dict()
# id -> number of -1s gotten without doing anything
idle_cycles = dict()

nat_ys_got = [] 
nat_ys_sent = [] 

computers = []
def get_input(computer_id):
  yield computer_id
  l = packets[computer_id]
  while True:
    if len(l) == 0:
      idle_cycles[computer_id] += 1
      yield -1
    else:
      idle_cycles[computer_id] = 0
      yield l.pop(0)

for i in range(50):
  packets[i] = []
  partials[i] = []
  idle_cycles[i] = 0
  computers.append(intcode.Computer(get_input(i)))

def is_done():
  if len(nat_ys_sent) < 2:
    return False
  if nat_ys_sent[-1] == nat_ys_sent[-2]:
    return True

def is_computer_idle(id):
  if len(packets[id]) == 0 and idle_cycles[id] >= 2: # 2 idle cycles is sufficient
    return True
  return False

def is_idle():
  return all([is_computer_idle(id) for id in range(50)])

def send_packet(packet, from_id):
  to_id = packet[0]
  # Send:
  if to_id == 255:
    partials[to_id] = [0, packet[1], packet[2]]
    nat_ys_got.append(packet[2])
  else:
    packets[to_id].append(packet[1])
    packets[to_id].append(packet[2])
  if from_id == 255:
    nat_ys_sent.append(packet[2])
  else:
    partials[from_id] = []

while not is_done():
  if is_idle():
    send_packet(partials[255], 255)
    idle_cycles[0] = 0
  for i in range(50):
    if is_computer_idle(i):
      continue
    val = computers[i].step()
    if val == None:
      continue
    partials[i].append(val)
    if len(partials[i]) == 3:
      send_packet(partials[i], i)
  else:
    continue
  break 


print("Part 1:")
print(nat_ys_got[0])
print("Part 2:")
print(nat_ys_sent[-1])
