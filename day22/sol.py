#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import math

# Did not fully solve this one in 2019, but came back to it with fresh eyes and thoroughly 
# enjoyed deriving the modular arithmetic solution.

fn = "./in.txt"
l = util.filetowordlistlist(fn)

# ("cut", int) | "newstack" | ("deal", int)
def words_to_command(words):
  if words[0] == "cut":
    return ("cut", int(words[1]))
  if words[1] == "with":
    return ("deal", int(words[3]))
  return "newstack"

actions = [words_to_command(x) for x in l]

num_cards_p1 = 10007
num_cards_p2 = 119315717514047
num_shuffles_p2 = 101741582076661

# Fixes a number to be in the range [0, num_cards), while keeping it congruent mod num_cards
def regulate(i, num_cards):
  return ((i % num_cards) + num_cards) % num_cards 

# Regulates both values 
def regulate_coeffs(coeffs, num_cards):
  return (regulate(coeffs[0], num_cards), regulate(coeffs[1], num_cards))

# Takes in (A, B) where AI + B congruent to J mod num_cards.
# I is input index, J is output index.
# Modifies A and B and returns them to reflect the effect of the action, while retaining
# congruence mod num_cards.
# action: ("cut", int) | "newstack" | ("deal", int)
def calc_modular_coeffs(coeffs, action, num_cards):
  if action == "newstack":
    return regulate_coeffs((coeffs[0] * -1, coeffs[1] * -1 - 1), num_cards)
  if action[0] == "cut":
    return regulate_coeffs((coeffs[0], coeffs[1] - action[1]), num_cards)
  # Action is deal
  return regulate_coeffs((coeffs[0] * action[1], coeffs[1] * action[1]), num_cards)

coeffs_p1 = (1, 0)
for action in actions:
  coeffs_p1 = calc_modular_coeffs(coeffs_p1, action, num_cards_p1)

print("Part 1:")
print((coeffs_p1[0] * 2019 + coeffs_p1[1]) % num_cards_p1)

def combine_modular_coeffs(coeffs1, coeffs2, num_cards):
  return regulate_coeffs((coeffs1[0] * coeffs2[0], coeffs1[0] * coeffs2[1] + coeffs1[1]), num_cards)

def repeat_modular_coeffs(coeffs, repeat, num_cards):
  if repeat == 0:
    return (1, 0)
  if repeat == 1:
    return coeffs
  if repeat % 2 == 0:
    half_coeffs = repeat_modular_coeffs(coeffs, repeat / 2, num_cards)
    return combine_modular_coeffs(half_coeffs, half_coeffs, num_cards)
  else:
    half_coeffs = repeat_modular_coeffs(coeffs, (repeat - 1) / 2, num_cards)
    return combine_modular_coeffs(combine_modular_coeffs(half_coeffs, half_coeffs, num_cards), coeffs, num_cards)

coeffs_p2 = (1, 0)
for action in actions:
  coeffs_p2 = calc_modular_coeffs(coeffs_p2, action, num_cards_p2)

coeffs_p2 = repeat_modular_coeffs(coeffs_p2, num_shuffles_p2, num_cards_p2)

def modular_inverse(a, n): # https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
  t = (0, 1)
  r = (n, a)
  while r[1] != 0:
    quotient = r[0] // r[1]
    t = (t[1], t[0] - quotient * t[1])
    r = (r[1], r[0] - quotient * r[1])
  if r[0] > 1:
    return None
  return t[0] if t[0] >= 0 else t[0] + n

inverse_coeff = modular_inverse(coeffs_p2[0], num_cards_p2)
ans = regulate((2020 - coeffs_p2[1]) * inverse_coeff, num_cards_p2)

print("Part 2:")
print(ans)
