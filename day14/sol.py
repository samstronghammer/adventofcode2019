#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import math

# I had a hard time with part 1, but part 2 was quick. I first thought of 
# integer programming (it looked like a set of constraints) but quickly
# realized it was the wrong path. I then got stuck for a while trying
# to decide how to handle the situation where resources would be wasted
# no matter what. Turns out that with the way the constraints for the
# problem are laid out, there aren't any cycles it seems. If there were
# we would have had trouble with the "still possible to produce" aspect
# of things. But, it worked out. The binary search for part 2 on the
# infinity of all numbers was interesting. I tried a couple deltas and 
# a million seemed to work fine.

fn = "./in.txt"

raw_eqns = util.filetolist(fn)
eqs = {}

for eq in raw_eqns:
	ins, outs = eq.split(" => ")
	lins = ins.split(", ")
	lin_pairs = []
	for inv in lins:
		numin, s = inv.split(" ")
		lin_pairs.append((int(numin), s))
	numout, s = outs.split(" ")
	eqs[s] = (int(numout), lin_pairs)


def get_possible(chem):
	possible = set()
	if chem == "ORE":
		return possible
	eq = eqs[chem]
	for inp in eq[1]:
		possible.add(inp[1])
		possible = possible.union(get_possible(inp[1]))
	return possible


def get_possible_from_dict(have_dict):
	possible = set()
	for key in have_dict:
		possible = possible.union(get_possible(key))
	return possible

def calc_ore_required(fuel):
	have = {}
	have["FUEL"] = fuel
	while True:
		newhave = {}
		done = True
		possible = get_possible_from_dict(have)
		for key in have:
			eq = eqs[key]
			oreout = False
			for inval in eq[1]:
				if inval[1] == "ORE":
					oreout = True
			if not oreout:
				done = False
				if key in possible:
					mult = int(math.floor(have[key] / eq[0]))
					rem = have[key] - mult * eq[0]
					if mult > 0:
						for inval in eq[1]:
							if not inval[1] in newhave:
								newhave[inval[1]] = 0
							newhave[inval[1]] += (mult * inval[0])
					if rem > 0:
						if not key in newhave:
							newhave[key] = 0
						newhave[key] += rem
				else:
					mult = int(math.ceil(have[key] / eq[0]))
					if mult > 0:
						for inval in eq[1]:
							if not inval[1] in newhave:
								newhave[inval[1]] = 0
							newhave[inval[1]] += (mult * inval[0])
			else:
				if not key in newhave:
					newhave[key] = 0
				newhave[key] += have[key]
		if done:
			break
		else:
			have = newhave

	totore = 0
	for key in have:
		eq = eqs[key]
		for inval in eq[1]:
			if inval[1] == "ORE":
				totore += math.ceil(have[key] / eq[0]) * inval[0]
			else:
				print("ERROR")
	return totore

print("Part 1")
print(calc_ore_required(1))
print("Part 2")
fuel = 0
delta = 1000000
cap = 1000000000000
while True:
	if calc_ore_required(fuel) > cap:
		fuel -= delta
		delta = delta // 2
	else:
		if calc_ore_required(fuel) <= cap and calc_ore_required(fuel + 1) > cap:
			break
		fuel += delta
print(fuel)
