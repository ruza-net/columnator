"""
This module contains various heuristics used to determine how to approximate given view
(split into possibly ambiguous columns using tab fill) using tabs.
"""

# Traverses a string until a sequence of `tab_fill` of length `tab_width`
#
def eat_section(tab_width, tab_fill, line):
	i = 0
	seen_blank_width = 0
	
	while i < len(line):
		# Count the tab fill
		#
		if line[i] == tab_fill:
			seen_blank_width += 1
		else:
			seen_blank_width = 0
		
		# Stop if we hit tab width
		#
		if seen_blank_width == tab_width:
			i -= tab_width - 1
			break
		
		i += 1
	
	return line[:i], line[i:]

# Skip any sequence of tab fill
#
def eat_blank(tab_width, tab_fill, line):
	i = 0
	while i < len(line) and line[i] == tab_fill:
		i += 1
	return i, line[i:]

# Split lines into rough columns, based solely on their tab fill separation
#
# Returns a list of lists, containing information about columns and
# their preceding tab fill length and "tab stop".
#
def split_sections(tab_width, tab_fill, lines):
	sections = []
	
	for line in lines:
		last_stop = 0
		last_width = 0
		section = []
		
		while len(line) > 0:
			# Separate the non-fill part of the line
			#
			sec, line = eat_section(tab_width, tab_fill, line)
			section.append((last_width, last_stop, sec))
			last_stop += len(sec)
			
			# Skip the rest of the tab fill
			#
			last_width, line = eat_blank(tab_width, tab_fill, line)
			last_stop += last_width
		
		# Trailing tab fill that is at least one tab width
		#
		if last_width >= tab_width:
			section.append((last_width, last_stop, ''))
		
		elif last_width > 0:
			raise ValueError('[unreachable] eat_section didn\'t eat trailing whitespace')
		
		sections.append(section if len(section) > 0 else [(0, 0, '')])
	
	return sections

# Split tabs based on neighbors' tab stops.
#
# Last two arguments are functions used to determine whether the current line index
# is still in bounds, and to compute the neighbor's index (since this function can
# be used both for forward and backward pass).
#
def splitting_pass(tab_width, col, secs, enumerated_secs, in_bounds, neighbor_idx):
	min_width = None
	
	for i, line in enumerated_secs:
		if len(line) > col:
			if in_bounds(i):
				neigh = secs[neighbor_idx(i)]
				
				# If neighbor has at least as many columns as current line
				#
				if len(neigh) > col:
					align_diff = line[col][1] - neigh[col][1]
					
					# If the difference of neighbor's and current alignment is to the left
					# of current column's start, and if it's at least a tab width long...
					#
					if align_diff < line[col][0] and align_diff > tab_width:
						# Split the current tab into two, one aligned at the neighbor's
						# tab stop.
						#
						secs[i] = (line[:col]
							+ [
								(line[col][0] - align_diff, neigh[col][1], ''),
								(align_diff, line[col][1], line[col][2])
							]
							+ line[col+1:])
			
			if min_width is None or min_width > secs[i][col][0]:
				min_width = secs[i][col][0]
	
	return min_width

# Split tab fills which consist of more than one tab.
# Computes when to split based on relative tab stop positions over adjacent lines.
# Uses both forward and backward pass to make the computation simple (and local).
#
# Returns updated information of the same format as in `split_sections`.
#
def split_compound_blanks(tab_width, secs):
	max_depth = max(len(line) for line in secs)
	
	# This is shared among all the calls to `splitting_pass`
	#
	ens = list(enumerate(secs))
	
	for col in range(max_depth):
		# Forward split
		#
		splitting_pass(
			tab_width,
			col,
			secs,
			ens,
			lambda i: i > 0,
			lambda i: i - 1,
		)
		
		# Backward split
		#
		splitting_pass(
			tab_width,
			col,
			secs,
			reversed(ens),
			lambda i: i < len(secs) - 1,
			lambda i: i+1,
		)
	
	return secs


# Replace sequences of tab fill determined to be column separators into tabs.
#
def desugar(tab_width, tab_fill, view):
	lines = view.split('\n')
	sections = split_sections(tab_width, tab_fill, lines)
	
	sections = split_compound_blanks(tab_width, sections)
	
	return '\n'.join('\t'.join(x[2] for x in line) for line in sections)
