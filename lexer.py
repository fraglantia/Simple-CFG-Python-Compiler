import re


def lex(s, rules):
	matches = []

	idx = 0
	groups = {}
	patterns = []

	for regex, name in rules:
		group_name = 'GROUP{}'.format(idx)
		patterns.append('(?P<{}>{})'.format(group_name, regex))
		groups[group_name] = name
		idx += 1

	full_pattern = re.compile('|'.join(patterns))
	# print(full_pattern)

	pos = 0

	while (pos < len(s)):
		m = full_pattern.match(s, pos)
		if m:
			group_name = m.lastgroup
			name = groups[group_name]
			matches.append((name, m.group(group_name), pos))
			pos = m.end()
		else:
			print('ERROR')
			break

	return matches


def lexer_run():
	rules = [
			('\n|\r\n',			'enter'),
			('\t|    ',			'tab'),
			(' ',				'space'),
			('\\bclass\\b',		'class'),
			('\\bimport\\b',	'import'),
			('\\bfrom\\b',		'from'),
			('\\bas\\b',		'as'),
			('\\bif\\b',		'if'),
			('\\belif\\b',		'elif'),
			('\\belse\\b',		'else'),
			('\\band|or\\b',	'boolop'),
			('\\bnot\\b',		'not'),
			('\\bTrue|False\\b','bool'),
			('\\bNone\\b',		'none'),
			('\\bfor\\b',		'for'),
			('\\bwhile\\b',		'while'),
			('\\bbreak\\b',		'break'),
			('\\bcontinue\\b',	'cont'),
			('\\bdef\\b',		'def'),
			('\\breturn\\b',	'return'),
			('\\bpass\\b',		'pass'),
			('\\braise\\b',		'raise'),
			('\\bwith\\b',		'with'),
			('\\bis\\b',		'is'),
			('\\bin\\b',		'in'),
			('#(.*)',			'commentline'),
			('"""[\s\S]*"""',	'multiline1'),
			("'''[\s\S]*'''",	'multiline2'),
			("'(.*)'",			'string1'),
			('"(.*)"',			'string2'),
			('\d+',				'number'),
			('\+=',				'plusassign'),
			('\-=',				'minassign'),
			('\*=',				'kaliassign'),
			('\/=',				'divassign'),
			('\/\/=',			'intdivassign'),
			('%=',				'modassign'),
			('&=',				'bitandassign'),
			('\|=',				'bitorassign'),
			('\^=',				'bitxorassign'),
			('>>=|<<=',			'shiftsassign'),
			('\*\*=',			'pangkatassign'),
			('[a-zA-Z_](\w+)?',	'identifier'),
			('\+',				'plus'),
			('%',				'mod'),
			('\-',				'min'),
			('\*\*',			'pangkat'),
			('>>|<<',			'bitshifts'),
			('\*',				'kali'),
			('&|\||\^',			'bitop'),
			('\/\/',			'intdiv'),
			('\/',				'div'),
			('\(',				'kbuka1'),
			('\)',				'ktutup1'),
			('\[',				'kbuka2'),
			('\]',				'ktutup2'),
			('\{',				'kbuka3'),
			('\}',				'ktutup3'),
			('!=',				'nequals'),
			('==',				'equals'),
			('<=',				'lte'),
			('>=',				'gte'),
			('=',				'assignment'),
			('<',				'lt'),
			('>',				'gt'),
			(':',				'colon'),
			(',',				'comma'),
			('.',				'dot'),
			('~',				'neg')
		]


	f = open('test.py')
	s = f.read()
	# print(s)
	# 

	matches = lex(s, rules)
	lang = [x[0] for x in matches]
	lang = [x for x in lang if x != 'tab']
	lang = [x for x in lang if x != 'space']
	lang.append('enter')

	return lang