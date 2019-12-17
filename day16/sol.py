#!/usr/bin/python3
import sys
sys.path.append("..")
import util
import math

# Very frustrating day. The first part was fine, I wish I'd used numpy though.
# I spent wayyyy too long down the wrong track on part 2. I didn't realize that
# the first 7 digits were taken from the *input*. I thought they were from 
# *after running fft 100 times*. I'd literally already written the back_half_fft
# function but hadn't figured out the general solution, which, as it turns out,
# is entirely unnecessary :) An excellent example of why to ALWAYS read the
# problem statement thoroughly!

def r(n):
	return n % 10 if n >= 0 else -n % 10

# Borrowed this from stack overflow
def dot(K, L):
	if len(K) != len(L):
		print("ERROR")
		return 0
	return sum(i[0] * i[1] for i in zip(K, L))

def get_patterns(l):
	patterns = {}
	base = [0, 1, 0, -1]
	for i in range(l):
		one_pat = []
		reps = i + 1
		for j in range(l + 1):
			realind = int(math.floor(j / reps)) % 4
			nextval = base[realind]
			one_pat.append(nextval)
		patterns[i] = one_pat[1:]
	return patterns

def fft(l, patterns):
	newl = []
	for i in range(len(l)):
		newl.append(r(dot(l, patterns[i])))
	return newl

def fft_num(l, num_times):
	patterns = get_patterns(len(l))
	for i in range(num_times):
		l = fft(l, patterns)
	return l

def first_8(l, num_times):
	ans = fft_num(l, num_times)[0:8]
	return "".join([str(x) for x in ans])

def back_half_fft(l):
	ans = []
	for i in range(len(l) - 2, -1, -1):
		l[i] = r(l[i + 1] + l[i])
	return l

fn = "./in.txt"
l = [int(x) for x in util.filetocharlist(fn)]
patterns = get_patterns(len(l))
print("Part 1")
print(first_8(l, 100))

offset = int("".join([str(x) for x in l[0:7]]))
correct_len = 10000
cut_off = 8000
newl = l * (correct_len - cut_off)
mod_offset = offset - len(l) * cut_off
for i in range(100):
	newl = back_half_fft(newl)
msg = newl[mod_offset:(mod_offset + 8)]
print("Part 2")
print("".join([str(x) for x in msg]))