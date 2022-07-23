import sys
import time
import shutil

from rendering import render
from fileworks import load, render_model, update_model


def print_usage():
	print('''USAGE:\n\tcolumnator <model_file> <view_file> [<tab_width> [<tab_fill>]]\n\t''')
	print('\t- <model_file> is a (possibly nonexistent) file in current directory')
	print('\t- <view_file> is a (possibly nonexistent) file in current directory')
	print('\t- <tab_width> is optionally an integer = the number of repeats of <tab_fill> used to render a tab (default = 4)')
	print('\t- <tab_fill> is optionally a character used in view file to render tab from model file (default = ` `)')
	sys.exit(1)


_, model_name, view_name, tab_width, tab_fill = \
	sys.argv + [4, ' '] if len(sys.argv) == 3 else \
	sys.argv + [' '] if len(sys.argv) == 4 else \
	sys.argv if len(sys.argv) == 5 else \
	print_usage()


try:
	tab_width = int(tab_width)
except ValueError:
	print_usage()

if len(tab_fill) != 1:
	print_usage()


example = r'''
asdf
as	dsa
	jwie	3u1	i2
sdreq3f	i3n	92j1i0ij30	jf
ai	93
	
asd0	02	kso9

asdhfiwuho
as	ieu
'''

print('INFO: Running columnator with following config:')
print(f'\ttab width = {tab_width}')
print(f'\tmodel file = {model_name}')
print(f'\tview file = {view_name}')
print(f'\ttab fill = `{repr(tab_fill)[1:-1]}`')
print()
print('INFO: The following text...')
print('\n\t'.join(example.split('\n')))
print('...would be rendered as follows:')
print('\n\t'.join(render(tab_width, tab_fill, example).split('\n')))


model = load(model_name)
render_model(tab_width, tab_fill, view_name, model)


model_will_update = False
view_will_update = False

while True:
	model = load(model_name)
	
	if model_will_update:
		render_model(tab_width, tab_fill, view_name, model)
		model_will_update = False
	
	elif model == '':
		print('INFO: model will update')
		model_will_update = True
	
	view = load(view_name)
	
	if view_will_update:
		update_model(tab_width, tab_fill, model_name, view)
		time.sleep(0.1)
		
		view_will_update = False
		model_will_update = True
	
	elif view == '':
		print('INFO: view will update')
		view_will_update = True
