def eat_section(tab_width, tab_fill, line):
	i = 0
	seen_blank_width = 0
	
	while i < len(line):
		if line[i] == tab_fill:
			seen_blank_width += 1
		else:
			seen_blank_width = 0
		
		if seen_blank_width == tab_width:
			i -= tab_width - 1
			break
		
		i += 1
	
	return line[:i], line[i:]

def eat_blank(tab_width, tab_fill, line):
	i = 0
	while i < len(line) and line[i] == tab_fill:
		i += 1
	return i, line[i:]

def split_sections(tab_width, tab_fill, lines):
	sections = []
	
	for line in lines:
		last_stop = 0
		last_width = 0
		section = []
		
		while len(line) > 0:
			sec, line = eat_section(tab_width, tab_fill, line)
			section.append((last_width, last_stop, sec))
			last_stop += len(sec)
			
			last_width, line = eat_blank(tab_width, tab_fill, line)
			last_stop += last_width
		
		if last_width >= tab_width:
			section.append((last_width, last_stop, ''))
		
		elif last_width > 0:
			raise ValueError('[unreachable] eat_section didn\'t eat trailing whitespace')
		
		sections.append(section if len(section) > 0 else [(0, 0, '')])
	
	return sections

def splitting_pass(tab_width, col, secs, enumerated_secs, in_bounds, neighbor_idx):
	min_width = None
	
	for i, line in enumerated_secs:
		if len(line) > col:
			if in_bounds(i):
				neigh = secs[neighbor_idx(i)]
				
				if len(neigh) > col:
					align_diff = line[col][1] - neigh[col][1]
					
					if align_diff < line[col][0] and align_diff > tab_width:
						secs[i] = (line[:col]
							+ [
								(line[col][0] - align_diff, neigh[col][1], ''),
								(align_diff, line[col][1], line[col][2])
							]
							+ line[col+1:])
						
			if min_width is None or min_width > secs[i][col][0]:
				min_width = secs[i][col][0]
	
	return min_width

def split_compound_blanks(tab_width, secs):
	max_depth = max(len(line) for line in secs)
	ens = list(enumerate(secs))
	
	for col in range(max_depth):
		splitting_pass(
			tab_width,
			col,
			secs,
			ens,
			lambda i: i > 0,
			lambda i: i - 1,
		)
		
		splitting_pass(
			tab_width,
			col,
			secs,
			reversed(ens),
			lambda i: i < len(secs) - 1,
			lambda i: i+1,
		)
	
	return secs


def desugar(tab_width, tab_fill, view):
	lines = view.split('\n')
	sections = split_sections(tab_width, tab_fill, lines)
	
	sections = split_compound_blanks(tab_width, sections)
	# sections = regroup_blanks(tab_width, sections)
	
	# import rendering
	# r = rendering.render(
	# 	tab_width,
	# 	tab_fill,
	# 	'[\n\t' + '\n\t'.join('[' + '\t'.join(str(x) for x in line) + ']' for line in sections) + '\n]'
	# )
	# return r
	return '\n'.join('\t'.join(x[2] for x in line) for line in sections)
