def group_sections(lines, col_idx):
	i = 0
	j = 0
	while i < len(lines):
		while j < len(lines) and len(lines[j]) > col_idx:
			j += 1
		
		if j - i > 0:
			yield i, j
		else:
			j += 1
		
		i = j

def merge_columns(tab_width, tab_fill, lines, col_idx):
	ret = lines
	for start,end in group_sections(lines, col_idx+1):
		section = merge_columns(tab_width, tab_fill, lines[start:end], col_idx + 1)
		
		align_at = tab_width + max(len(line[col_idx]) for line in section)
		for i in range(len(section)):
			if col_idx + 1 < len(section[i]):
				indent = tab_fill * (align_at - len(section[i][col_idx]))
				section[i] = section[i][:col_idx] + [ section[i][col_idx] + indent + section[i][col_idx + 1] ]
		
		ret[start:end] = section
	
	return ret

def render(tab_width, tab_fill, model):
	lines = [line.split('\t') for line in model.split('\n')]
	
	lines = merge_columns(tab_width, tab_fill, lines, 0)
	
	return '\n'.join(sum(lines, start=[]))
