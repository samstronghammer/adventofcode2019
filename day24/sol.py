#!/usr/bin/python3
import sys
sys.path.append("..")
import util

# Didn't finish this in 2019. The solution is rather hard-coded, would be interesting
# to see something that more robustly connects the recursive layers.

fn = "./in.txt"
charlistlist = util.filetocleancharlistlist(fn)

locs = {}
locs_2 = set()
loc_list = []
num_rows = len(charlistlist)
num_cols = len(charlistlist[0])

for row in range(num_rows):
  charlist = charlistlist[row]
  for col in range(num_cols):
    c = charlist[col]
    loc_list.append((row, col))
    locs[(row, col)] = c
    if c == "#":
      locs_2.add((row, col, 0))

def locs_to_key(l):
  s = ""
  for loc in loc_list:
    s += l[loc]
  return s

def step(l):
  newl = {}
  for loc in loc_list:
    num_adj = 0
    for adj in util.adj4(loc):
      bug = l.get(adj, ".")
      if bug == "#":
        num_adj += 1
    newl[loc] = "#" if num_adj == 1 or (num_adj == 2 and l[loc] == ".") else "."
  return newl

def biodiversity(l):
  key = locs_to_key(l)
  tot = 0
  for i in range(len(key)):
    if key[i] == ".":
      continue
    tot += 2 ** i
  return tot

seen = set()
curr_locs = locs
while True:
  key = locs_to_key(curr_locs)
  if key in seen:
    break
  seen.add(key)
  curr_locs = step(curr_locs)

print("Part 1")
print(biodiversity(curr_locs))


# location: (row, col, depth)
# starts with depth = 0, smaller is deeper, bigger is less deep.
def adj_locs(loc):
  ans = []
  level_loc = (loc[0], loc[1])
  for adj in util.adj4(level_loc):
    if adj == (2, 2):
      # Recurse in
      if loc[0] == 1:
        # To top
        ans.extend([(0, x, loc[2] + 1) for x in range(num_cols)])
      elif loc[0] == 3:
        # To bottom 
        ans.extend([(num_rows - 1, x, loc[2] + 1) for x in range(num_cols)])
      elif loc[1] == 1:
        # To left
        ans.extend([(x, 0, loc[2] + 1) for x in range(num_rows)])
      elif loc[1] == 3:
        # To right 
        ans.extend([(x, num_cols - 1, loc[2] + 1) for x in range(num_rows)])
      else:
        raise "IMPOSSIBLE"
    elif adj[0] < 0:
      # to 8
      ans.append((1, 2, loc[2] - 1))
    elif adj[1] < 0:
      # to 12
      ans.append((2, 1, loc[2] - 1))
    elif adj[0] >= num_rows:
      # to 18
      ans.append((3, 2, loc[2] - 1))
    elif adj[1] >= num_cols:
      # to 14
      ans.append((2, 3, loc[2] - 1))
    else:
      # Ok
      ans.append((adj[0], adj[1], loc[2]))
  return ans

def step_2(l):
  newl = set()
  neighbors = set()
  for loc in l:
    neighbors.add(loc)
    for adj in adj_locs(loc):
      neighbors.add(adj)

  for loc in neighbors:
    num_adj = 0
    for adj in adj_locs(loc):
      if adj in l:
        num_adj += 1
    if num_adj == 1 or (num_adj == 2 and not loc in l):
      newl.add(loc)
  return newl

curr_bugs = locs_2
for i in range(200):
  curr_bugs = step_2(curr_bugs)

print("Part 2")
print(len(curr_bugs))
    
