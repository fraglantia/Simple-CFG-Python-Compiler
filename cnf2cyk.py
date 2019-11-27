from cfg2cnf import *
from lexer import *
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
		print("{:.2f}%".format(100*i/(len(s)+1)))
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

def is_pre_arr(arr1, arr2):
	# len(arr2) >= len(arr1)
	for i in range(len(arr1)):
		if(arr1[i] != arr2[i]):
			return False
	return True

def find_last_acc(s):
	global cyk

	line = 1

	for el in cyk:
		if(start_symbol in el[1]):
			if(is_pre_arr(el[0], s)):
				line = el[0].count('enter')

	return line+1


# tampilkan kesalahan ===========

def compile_CYK(path):
	global cyk, terminals, variables, rules, start_symbol
	s = lexer_run(path)
	print(s)

	t = time.time()
	terminals, variables, rules, start_symbol = generate_cnf()

	print("cnf generated in {:.2f} seconds".format(time.time()-t))
	print()
	cyk = []


	t = time.time()

	print("generating cyk:")

	build_cyk(s)

	# pretty_print_rules()

	# for el in cyk:
	# 	print(el)

	verdict = (start_symbol in get_val(s, cyk))

	print()
	print("Verdict:")

	if(verdict):
		print('Accepted')
	else:
		print('Syntax Error')
		print("error at line {}!".format(find_last_acc(s)))

	print("cyk generated in {:.2f} seconds".format(time.time()-t))
