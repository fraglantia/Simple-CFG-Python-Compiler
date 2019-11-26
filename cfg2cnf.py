# CFG FROM FILE
import copy
import itertools

def load_terminals(filename='./assets/terminals.txt'):
	# TERMINALS AS ARRAY (newline seperated)
	f = open(filename)
	data = f.read()
	terminals = data.split('\n')
	f.close()
	return terminals

def load_rules(filename='./assets/rules.txt'):
	# RULES AS AN ARRAY OF TUPLES, STATE AND VALUE (STATE -> A;B | c;d, newline seperated), * in state = start
	# referensi rules dari https://docs.python.org/3.7/reference/grammar.html
	f = open(filename)
	data = f.read()
	lines = data.split('\n')
	f.close()

	variables = []

	start_symbol = ''
	rules = {}

	for line in lines:
		key, arr = line.split(' -> ')
		arr = arr.split(' | ')

		new_arr = []
		for elmt in arr:
			new_arr.append(elmt.split(';'))

		if(start_symbol == '' and key[0] == '*'):
			key = key[1:]
			start_symbol = key

		rules[key] = new_arr
		variables.append(key)

	# print(rules)

	return variables, rules, start_symbol

def load_CFG():
	global rules, variables, terminals, start_symbol
	terminals, (variables, rules, start_symbol) = load_terminals(), load_rules()

# ===================================================================

def find_indexes(n, arr):
	ret = []
	for i, val in enumerate(arr):
		if val == n:
			ret.append(i)
	return ret

def permute(arr):
	# [0,4] => [ [0,4], [0], [4], []   ]
	res = []
	for i in range(len(arr)+1):
		listup = list(itertools.combinations(arr, i))
		for el in listup:
			res.append(list(el))
	return res

# ===================================================================

def pretty_print_rules():
	global rules, variables, terminals, start_symbol
	for var in rules:
		rule = rules[var]

		if(var == start_symbol):
			s = '*'
		else:
			s = ''

		s += var + ' -> '

		rightside = []
		for ar in rule:
			rightside.append(' '.join(ar))

		s += ' | '.join(rightside)

		print(s)

def rule_contains(v_or_t, rule):
	global rules, variables, terminals, start_symbol
	# second part of tuple
	for arr in rule:
		if(v_or_t in arr):
			return True
	return False

def find_variables(rule):
	global rules, variables, terminals, start_symbol
	rule_var = []
	for arr in rule:
		for var in arr:
			if(var in variables and not(var in rule_var)):
				rule_var.append(var)
	
	return rule_var

def find_terminals(rule):
	global rules, variables, terminals, start_symbol
	rule_term = []
	for arr in rule:
		for term in arr:
			if(term in terminals and not(term in rule_term)):
				rule_term.append(term)
	
	return rule_term

# ===================================================================

def remove_variable(var, rule):
	# var is nullable
	global rules, variables, terminals, start_symbol
	# [[A,B,c], [A]]
	new_rule = []

	for production in rule:
		new_production = [n for n in production if n != var]
		new_rule.append(new_production)

	return new_rule


def remove_null_prod(var, production):
	global rules, variables, terminals, start_symbol
	# var is nullable e.g. A
	# production is an array e.g. [A, B, A, c]
	# retval is array of array [[A, B, A, c], [B, A, c], [A, B, c], [B, c]]
	res = []
	idxs = find_indexes(var, production)
	perm = permute(idxs)
	for arr in perm:
		p = production.copy()
		for el in arr:
			p[el] = ''

		p = [n for n in p if n != '']
		res.append(p)

	while(['eps'] in res):
		res.remove(['eps'])

	while([] in res):
		res.remove([])

	return res


def remove_null(var, rule):
	# var is nullable
	global rules, variables, terminals, start_symbol
	# [[A,B,c], [A]]
	new_rule = []

	for production in rule:
		new_production = remove_null_prod(var, production)
		for el in new_production:
			if el not in new_rule:
				new_rule.append(el)

	return new_rule

def single_epsilon():
	res = []
	for var in rules:
		rule = rules[var]
		if(len(rule) == 1 and rule_contains('eps', rule)):
			res.append(var)
	return res


def rule_contains_null(nulls, rule):
	global rules, variables, terminals, start_symbol

	

	production_null = False

	for production in rule:
		local_null = True
		for el in production:
			
			if(el not in nulls):
				local_null = False
				break

		if(local_null):
			production_null = True
			break

	return production_null




def nullables():
	global rules, variables, terminals, start_symbol

	null_list = []
	new_rules = copy.deepcopy(rules)

	for i in range(len(variables)):
		for var in new_rules:
			rule = new_rules[var]

			nullable = False

			if(rule_contains_null(null_list, rule)):
				nullable = True

			if(rule_contains('eps', rule)):
				nullable = True

			if(var not in null_list and nullable):
				null_list.append(var)

	return null_list


def eliminate_null():
	global rules, variables, terminals, start_symbol

	epsilons = single_epsilon()
	while(len(epsilons) != 0):
		for ep_var in epsilons:
			for var in rules:
				rule = rules[var].copy()
				rules[var] = remove_variable(ep_var, rule)
			del rules[ep_var]

		epsilons = single_epsilon()

	null_list = nullables()
	for var in rules:
		for null_var in null_list:
			rule = rules[var].copy()
			rules[var] = remove_null(null_var, rule)

# ===================================================================

def remove_single(var, rule):
	global rules, variables, terminals, start_symbol
	# var = A
	# [[A,B,c], [A]] => [[A,B,C]]
	new_rule = []

	for production in rule:
		if not(len(production) == 1 and production[0] == var):
			new_rule.append(production)

	return new_rule


def rule_union(rule1, rule2):
	global rules, variables, terminals, start_symbol
	a = set(tuple(n) for n in rule1)
	b = set(tuple(n) for n in rule2)

	new_rule = [list(item) for item in set(tuple(row) for row in a.union(b))]	
	new_rule = [n for n in new_rule if n != []]

	return new_rule


def unitaries():
	global rules, variables, terminals, start_symbol

	new_rules = copy.deepcopy(rules)

	unit_dict = {}
	for var in new_rules:
		rule = new_rules[var]
		unitary_to = []
		for ar in rule:
			if(len(ar) == 1):
				item = ar[0]
				if(item in variables):
					unitary_to.append(item)

		if(len(unitary_to) != 0):
			unit_dict[var] = unitary_to

	return unit_dict


def eliminate_unit():
	global rules, variables, terminals, start_symbol

	unit_d = unitaries()
	while(len(unit_d) != 0):
		for key in unit_d:
			eliminate_vals = unit_d[key]
			for el in eliminate_vals:
				rule = rules[key].copy()
				rule = remove_single(el, rule)
				if(key != el):
					rules[key] = rule_union(rule, rules[el])
				else:
					rules[key] = rule

		unit_d = unitaries()

# ===================================================================

def find_nonsingle(rule):
	res = []
	for ar in rule:
		for t in terminals:
			if(len(ar) > 1 and t in ar):
				res.append(t)

	return res

def replace_nonsingle(rule, term, var):
	global rules, variables, terminals, start_symbol

	res = []

	new_rule = rule.copy()
	for ar in new_rule:
		if(len(ar) > 1 and term in ar):
			new_ar = [x if x != term else var for x in ar]
			res.append(new_ar)
		else:
			res.append(ar)

	return res

def get_nonsing_rule(nonsing, additional_rules):
	# returns key to a rule of single
	global rules, variables, terminals, start_symbol, ctr

	hit = [key for key, arr in rules.items() if arr == [nonsing]]
	hit += [key for key, arr in additional_rules.items() if arr == [nonsing]]

	if(len(hit) == 0):
		k = '_' + str(ctr)
		additional_rules[k] = [nonsing]
		variables.append(k)
		ctr += 1
		return k

	else:
		return hit[0]



def eliminate_nonsingle_term():
	global rules, variables, terminals, start_symbol, ctr

	additional_rules = {}

	for val in rules:
		rule = rules[val].copy()
		nonsingles = find_nonsingle(rule)
		for nonsing in nonsingles:
			k = get_nonsing_rule([nonsing], additional_rules)
			rule = replace_nonsingle(rule, nonsing, k)

		rules[val] = rule

	rules.update(additional_rules)


# ===================================================================

def get_nondouble_rule(double, additional_rules):
	# double is [A,B]
	global rules, variables, terminals, start_symbol, ctr

	hit = [key for key, arr in rules.items() if arr == double]
	hit += [key for key, arr in additional_rules.items() if arr == double]

	if(len(hit) == 0):
		k = '_' + str(ctr)
		additional_rules[k] = double
		variables.append(k)
		ctr += 1
		return k
	else:
		return hit[0]

def replace_nondouble_prod(nondouble, additional_rules):
	# nondouble is [A,B,C] / [A,B,C,D]
	global rules, variables, terminals, start_symbol, ctr

	nondouble_copy = nondouble.copy()

	while (len(nondouble_copy) != 2):
		double = nondouble_copy[:2]
		rest = nondouble_copy[2:]

		# print(double, rest)

		nondouble_copy = [get_nonsing_rule(double, additional_rules)] + rest

	return nondouble_copy

def replace_nondouble_rule(rule, additional_rules):
	global rules, variables, terminals, start_symbol, ctr
	new_rule = []
	for prod in rule:
		if(len(prod) > 2):
			new_rule.append(replace_nondouble_prod(prod, additional_rules))
		else:
			new_rule.append(prod)

	return new_rule



def eliminate_nondouble_var():
	global rules, variables, terminals, start_symbol, ctr

	additional_rules = {}

	for val in rules:
		rule = rules[val].copy()
		rules[val] = replace_nondouble_rule(rule, additional_rules)

	rules.update(additional_rules)

# ===================================================================


def generate_cnf():
	global rules, variables, terminals, start_symbol, ctr
	ctr = 0
	load_CFG()
	eliminate_null()	
	eliminate_unit()
	eliminate_nonsingle_term()
	eliminate_nondouble_var()
	# pretty_print_rules()
	return terminals, variables, rules, start_symbol