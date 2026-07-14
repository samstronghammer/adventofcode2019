#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import networkx as nx

def get_distances(graph, important_locations):
  important_location_distances = {}
  for k in important_locations:
    # if it's a door, allow out edges for just this door
    node = important_locations[k]
    is_door = k.isupper()
    if is_door:
      for node2 in util.adj4(node):
        if not node2 in graph.nodes:
          continue
        graph.add_edge(node, node2, weight=1)

    all_path_lengths = nx.single_source_dijkstra_path_length(graph, important_locations[k])
    important_location_distances[k] = all_path_lengths

    # remove the added door edges
    if is_door:
      for node2 in util.adj4(node):
        if not node2 in graph.nodes:
          continue
        graph.remove_edge(node, node2)
  return important_location_distances

file_name = "./in.txt"
l = util.filetolist(file_name)
robot_chars = ["1", "2", "3", "4"]

def get_minimum_distance(is_p2):
  locs = {}
  for y in range(len(l)):
    for x in range(len(l[y])):
      locs[(x, y)] = l[y][x]

  important_locations = {}
  G = nx.DiGraph()

  # fill in nodes
  for key in locs:
    c = locs[key]
    if c == "#":
      continue
    if c != ".":
      important_locations[c] = key
    G.add_node(key)

  if is_p2:
    start_loc = important_locations["@"]
    del important_locations["@"]
    locs[start_loc] = "#"
    G.remove_node(start_loc)
    adj_4 = util.adj4(start_loc)
    adj_8 = util.adj8(start_loc)
    robots = robot_chars.copy()
    for adj in adj_8:
      if adj in adj_4:
        G.remove_node(adj)
        locs[adj] = "#"
      else:
        bot = robots.pop()
        locs[adj] = bot
        important_locations[bot] = adj

  for node in G.nodes:
    for node2 in util.adj4(node):
      if not node2 in G.nodes:
        continue
      G.add_edge(node, node2, weight=1)

  # doors need to ONLY have in-edges
  for key in important_locations:
    if not key.isupper():
      continue
    node = important_locations[key]
    for node2 in util.adj4(node):
      if not node2 in G.nodes:
        continue
      G.remove_edge(node, node2)

  important_location_distances = get_distances(G, important_locations) # {important key: {location: distance}}
  G2 = nx.Graph()
  for key in important_locations:
    node = important_locations[key]
    for key2 in important_locations:
      if key == key2:
        continue
      node2 = important_locations[key2]
      dist = important_location_distances.get(key).get(node2)
      if dist == None:
        continue
      G2.add_edge(key, key2, weight=dist)

  def calc_edges_to_change_to_remove_node(graph, key):
    if not graph.has_node(key):
      return ([], []) 
    edges_to_add = []
    edges_to_remove = []
    neighbors = list(graph.neighbors(key))
    for i in range(len(neighbors)):
      for j in range(len(neighbors)):
        if j <= i:
          continue
        n1 = neighbors[i]
        n2 = neighbors[j]
        old_edge_data = graph.get_edge_data(n1, n2)
        old_dist = float("inf") 
        if old_edge_data != None:
          old_dist = old_edge_data["weight"]
        new_dist = graph.get_edge_data(key, n1)["weight"] + graph.get_edge_data(key, n2)["weight"]
        if new_dist < old_dist:
          if old_edge_data != None:
            edges_to_remove.append((n1, n2, old_dist))
          edges_to_add.append((n1, n2, new_dist))
    removed_node_edges = list((x[0], x[1], x[2]["weight"]) for x in graph.edges(key, data=True))
    edges_to_remove.extend(removed_node_edges)
    return (edges_to_add, edges_to_remove) 

  def roll_forward(graph, mods):
    for edge in mods[1]:
      graph.remove_edge(edge[0], edge[1])
    for edge in mods[0]:
      graph.add_edge(edge[0], edge[1], weight=edge[2])

  def roll_back(graph, mods):
    for edge in mods[0]:
      graph.remove_edge(edge[0], edge[1])
    for edge in mods[1]:
      graph.add_edge(edge[0], edge[1], weight=edge[2])

  cache = {}

  def calc_key(graph, curr_locations):
    nodes = list(graph.nodes())
    nodes.sort()
    sorted_locations = sorted(curr_locations)
    return (tuple(nodes), tuple(sorted_locations))

  def find_best_path(graph, curr_locations, upperbound):
    cache_key = calc_key(graph, curr_locations)
    if cache.get(cache_key) != None:
      return cache.get(cache_key)
    neighbors = []
    for loc in curr_locations:
      some_neighbors = map(lambda n: (loc, n), graph.neighbors(loc))
      neighbors.extend(some_neighbors)
    options = []
    mod_graphs = {}
    for neighbor in neighbors:
      if neighbor[1].isupper():
        continue
      walk_to_neighbor_dist = graph.get_edge_data(neighbor[0], neighbor[1])["weight"]
      options.append((neighbor[0], neighbor[1], walk_to_neighbor_dist))
      if mod_graphs.get(neighbor[0]) == None:
        mod_graphs[neighbor[0]] = calc_edges_to_change_to_remove_node(graph, neighbor[0])
    if len(options) == 0:
      return 0
    options.sort(key=lambda x: x[2]) # closest first
    my_upperbound = upperbound
    best_path_length = float("inf")
    for option in options:
      neighbor = option[1]
      walk_to_neighbor_dist = option[2]
      if walk_to_neighbor_dist > my_upperbound:
        continue
      mod_1_tuple = mod_graphs[option[0]]
      roll_forward(graph, mod_1_tuple)
      graph.remove_node(option[0])
      mod_2_tuple = calc_edges_to_change_to_remove_node(graph, neighbor.upper())
      roll_forward(graph, mod_2_tuple)
      graph.remove_node(neighbor.upper())

      new_length = walk_to_neighbor_dist + find_best_path(graph, [neighbor if x == option[0] else x for x in curr_locations], my_upperbound - walk_to_neighbor_dist)
      if new_length < best_path_length:
        best_path_length = new_length
        my_upperbound = best_path_length

      roll_back(graph, mod_2_tuple)
      roll_back(graph, mod_1_tuple)

    cache[cache_key] = best_path_length
    return best_path_length
  if is_p2:
    return find_best_path(G2, robot_chars, float("inf"))
  else:
    return find_best_path(G2, ["@"], float("inf"))

print("Part 1:")
print(get_minimum_distance(False))
print("Part 2:")
print(get_minimum_distance(True))
