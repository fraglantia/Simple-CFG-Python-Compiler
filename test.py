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