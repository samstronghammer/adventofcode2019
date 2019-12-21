#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import math
import networkx as nx

def get_key_map(graph, keylocs):
	key_map = {}
	for k in keylocs:
		key_map[k] = {}
		for k2 in keylocs:
			if k != k2:
				if k2 in key_map and k in key_map[k2]:
					key_map[k][k2] = key_map[k2][k]
				else:
					key_map[k][k2] = nx.bidirectional_dijkstra(graph, keylocs[k], keylocs[k2])[0]
	return key_map

memoized = {}

def key_set_min_dist(key_set, key_map):
	if len(key_set) < 2:
		return 0
	tup = tuple(sorted(key_set))
	if tup in memoized:
		return memoized[tup]
	all_dists = []
	for k in key_set:
		min_dist = None
		for k2 in key_set:
			if k != k2:
				dist = key_map[k][k2]
				if min_dist == None or dist < min_dist:
					min_dist = dist
		all_dists.append(min_dist)
	# could be subtract max? Unsure.
	memoized[tup] = sum(all_dists) - min(all_dists)
	return memoized[tup]

def min_dist_to_finish(currloc, graph, keylocs, doorlocs, depth, rope, key_map):
	if rope != None and rope < 0:
		return None

	if rope != None and key_set_min_dist(keylocs.keys(), key_map) > rope:
		return None

	if len(keylocs) == 0:
		return 0

	min_dist = None

	# print(zipped)
	for k in keylocs:
		# print(depth)
		# if depth == 0:
		# 	print(min_dist)
		if depth < 20 and min_dist != None:
			print("depth:",depth,"dist:",min_dist)
		# print("locs",keylocs)
		try:
			path = nx.bidirectional_dijkstra(graph, currloc, keylocs[k])
			pathlen = path[0]
			keylocs_val = keylocs[k]
			keylocs.pop(k)
			doorlocs_val = None
			edges_added = []
			if k.upper() in doorlocs:
				free_pos = doorlocs[k.upper()]
				for loc in util.adj4(free_pos):
					if loc in graph.nodes and not loc in doorlocs.values():
						edges_added.append((free_pos, loc))
				graph.add_edges_from(edges_added, weight=1)
				doorlocs_val = doorlocs[k.upper()]
				doorlocs.pop(k.upper())
			ropetogive = None
			if min_dist == None:
				if rope != None:
					ropetogive = rope - pathlen
			else:
				ropetogive = min_dist - pathlen
			res = min_dist_to_finish(keylocs_val, graph, keylocs, doorlocs, depth + 1, ropetogive, key_map)
			if res != None:
				new_min_dist = pathlen + res
				if min_dist == None or new_min_dist < min_dist:
					min_dist = new_min_dist
			keylocs[k] = keylocs_val
			if doorlocs_val != None:
				for e in edges_added:
					graph.remove_edges_from(edges_added)
				doorlocs[k.upper()] = doorlocs_val
		except nx.NetworkXNoPath:
			continue
	return min_dist




fn = "./in.txt"

l = util.filetolist(fn)

locs = {}
for y in range(len(l)):
	for x in range(len(l[y])):
		locs[(x, y)] = l[y][x]

currloc = None
keylocs = {}
doorlocs = {}
G = nx.Graph()

for key in locs:
	c = locs[key]
	if c != "#":
		if c != ".":
			if c == "@":
				currloc = key
			elif c.islower():
				keylocs[c] = key
			else:
				assert c.isupper()
				doorlocs[c] = key
		G.add_node(key)

def invalid(c):
	return c.isupper()

for node in G.nodes:
	for node2 in util.adj4(node):
		if node2 in G.nodes:
			G.add_edge(node, node2, weight=1)

key_map = get_key_map(G, keylocs)

for node in G.nodes:
	for node2 in util.adj4(node):
		if node2 in G.nodes and (invalid(locs[node]) or invalid(locs[node2])):
			if (node, node2) in G.edges:
				G.remove_edge(node, node2)

# print(currloc)
# print(G.nodes)
# print(G.edges)

accessible_keys = set()
blocked_keys = set()
for k in keylocs:
	try:
		nx.bidirectional_dijkstra(G, currloc, keylocs[k])
		accessible_keys.add(k)
	except nx.NetworkXNoPath:
		blocked_keys.add(k)
		continue

print(accessible_keys)
print(blocked_keys)
print(key_map)
print("Part 1")
print(min_dist_to_finish(currloc, G, keylocs, doorlocs, 0, None, key_map))

