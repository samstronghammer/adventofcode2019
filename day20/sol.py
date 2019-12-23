#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import math
import networkx as nx

# Fun puzzle! I'm getting a lot more comfortable with networkx. Pretty
# much all of my bugs today were with off-by-one errors or typos, so 
# it went pretty smoothly.

fn = "./in.txt"
l = util.filetorawlist(fn)
G = nx.Graph()
for r in range(len(l)):
	for c in range(len(l[r])):
		if l[r][c] == ".":
			G.add_node((r, c))

for node in G.nodes:
	for node2 in util.adj4(node):
		if node2 in G.nodes:
			G.add_edge(node, node2)

inner_portals = {}
outer_portals = {}
for r in range(2, len(l) - 2):
	for c in range(2, len(l[r]) - 2):
		if l[r][c] == ".":
			portal_text = None
			if l[r][c - 1].isupper() and l[r][c - 2].isupper():
				portal_text = l[r][c - 2] + l[r][c - 1]
			elif l[r][c + 1].isupper() and l[r][c + 2].isupper():
				portal_text = l[r][c + 1] + l[r][c + 2]
			elif l[r - 1][c].isupper() and l[r - 2][c].isupper():
				portal_text = l[r - 2][c] + l[r - 1][c]
			elif l[r + 1][c].isupper() and l[r + 2][c].isupper():
				portal_text = l[r + 1][c] + l[r + 2][c]
			if portal_text != None:
				portal_loc = (r, c)
				outer = False
				if r == 2 or r == len(l) - 3 or c == 2 or c == len(l[r]) - 4:
					outer = True
				if outer:
					outer_portals[portal_text] = portal_loc
				else:
					inner_portals[portal_text] = portal_loc

start_loc = outer_portals["AA"]
end_loc = outer_portals["ZZ"]
for p in inner_portals:
	G.add_edge(inner_portals[p], outer_portals[p])

path = nx.bidirectional_dijkstra(G, start_loc, end_loc)
pathlen = path[0]

print("Part 1")
print(pathlen)
# The maximum depth hit by the path is 33
max_depth = 50

rec_G = nx.Graph()
for depth in range(max_depth):
	for n in G.nodes:
		rec_G.add_node((n[0], n[1], depth))

for node in rec_G:
	for node2 in util.adj4(node[0:2]):
		if (node2[0], node2[1], node[2]) in rec_G.nodes:
			rec_G.add_edge(node, (node2[0], node2[1], node[2]))


for depth in range(max_depth - 1):
	for p in inner_portals:
		inner_loc = inner_portals[p]
		outer_loc = outer_portals[p]
		# print((inner_loc[0], inner_loc[1], depth), (outer_loc[0], outer_loc[1], depth + 1))
		rec_G.add_edge((inner_loc[0], inner_loc[1], depth), (outer_loc[0], outer_loc[1], depth + 1))

path2 = nx.bidirectional_dijkstra(rec_G, (start_loc[0], start_loc[1], 0), (end_loc[0], end_loc[1], 0))
pathlen2 = path2[0]
print("Part 2")
print(pathlen2)