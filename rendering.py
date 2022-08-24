"""
This module renders tabs into aligned sequences of tab_fill.
"""

# Compute section boundaries for the given column index
#
def group_sections(lines, col_idx):
	i = 0
	j = 0
	while i < len(lines):
		# Expand downwards until we hit section boundary
		#
		while j < len(lines) and len(lines[j]) > col_idx:
			j += 1
		
		if j - i > 0:
			yield i, j
		else:
			j += 1
		
		# Jump to bottom margin
		#
		i = j

# Merge adjacent columns (around given column index) together, filling the gap with the right amount of tab fill.
#
# `lines` is a list of lists, representing lines consisting of columns
#
# Returns a list of lists, with the columns merged.
#
def merge_columns(tab_width, tab_fill, lines, col_idx):
	ret = lines
	for start,end in group_sections(lines, col_idx+1):
		# Merge all the further columns
		#
		section = merge_columns(tab_width, tab_fill, lines[start:end], col_idx + 1)
		
		# Compute the index of the rightmost tab fill character
		#
		align_at = tab_width + max(len(line[col_idx]) for line in section)
		
		for i in range(len(section)):
			if col_idx + 1 < len(section[i]):
				# Compute the gap between current column's right and the `align_at` index; fill it with tab fill.
				#
				indent = tab_fill * (align_at - len(section[i][col_idx]))
				
				# Replace this lines' trailing contents with the last two columns merged with the indent
				#
				section[i] = section[i][:col_idx] + [ section[i][col_idx] + indent + section[i][col_idx + 1] ]
		
		ret[start:end] = section
	
	return ret

# Merge all columns with align
#
def render(tab_width, tab_fill, model):
	lines = [line.split('\t') for line in model.split('\n')]
	
	lines = merge_columns(tab_width, tab_fill, lines, 0)
	
	return '\n'.join(sum(lines, start=[]))
