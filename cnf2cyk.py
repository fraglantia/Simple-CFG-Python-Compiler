from cfg2cnf import *
import itertools
import time

def generate_sub(s, l):
	assert l <= len(s)
	ar = []
	for i in range(len(s)-l+1):
		ar.append(s[i:i+l])

	return ar

def get_keys(rules, val):
	keys = []
	for key in rules:
		rule = rules[key]
		for prod in rule:
			if(prod == val):
				keys.append(key)
	return keys

def get_val(key, cyk):
	for el in cyk:
		if(el[0] == key):
			return el[1]
			break
	return None

def split_halves(s):
	res = []
	for i in range(1,len(s)):
		res.append((list(s[:i]), list(s[i:])))

	return res

def list_possibilities(ar1, ar2):
	res = []
	tups = list(itertools.product(ar1, ar2))
	for tup in tups:
		res.append(list(tup))

	return res


# build cyk =====================

def init_cyk(s):
	global rules, cyk
	arr = generate_sub(s, 1)

	for el in arr:
		vals = get_keys(rules, list(el))
		cyk.append((list(el),vals))

	cyk = [el for i, el in enumerate(cyk) if el not in cyk[:i]]


def build_cyk(s):
	global rules, cyk

	init_cyk(s)

	for i in range(2, len(s)+1):
		arr = generate_sub(s, i)
		for el in arr:
			sub = split_halves(el)
			# print()
			res = []
			for tup in sub:
				left = get_val(tup[0], cyk)
				right = get_val(tup[1], cyk)
				poss = list_possibilities(left, right)
				for pos in poss:
					vals = get_keys(rules, pos)
					for val in vals:
						if(val not in res):
							res.append(val)

			addition = (list(el),res)
			# print(addition)
			if(addition not in cyk):
				cyk.append(addition)


# build cyk =====================


def find_last_acc():
	global cyk

	line = 1

	for el in cyk:
		if(start_symbol in el[1]):
			line = el[0].count('enter')

	return line


# tampilkan kesalahan ===========

t = time.time()
terminals, variables, rules, start_symbol = generate_cnf()

print("cnf generated in {:.2f} seconds".format(time.time()-t))

cyk = []

f = open('./test.py')
s = list(f.read())
s = ['enter' if x == '\n' else x for x in s]
s = ['tab' if x == '\t' else x for x in s]
# print(s)


t = time.time()

build_cyk(s)


# print(cyk)

# for el in cyk:
# 	print(el)

print()

verdict = (start_symbol in get_val(s, cyk))

if(verdict):
	print('Accepted')
else:
	print('Syntax Error')
	print("error at line {}!".format(find_last_acc()))

print()
print("cyk generated in {:.2f} seconds".format(time.time()-t))
