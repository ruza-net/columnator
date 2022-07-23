from viewing import desugar
from rendering import render

def load(f_name):
	with open(f_name, 'r') as f:
		return ''.join(f.readlines())

def render_model(tab_width, tab_fill, view_name, model):
	with open(view_name, 'w') as view:
		view.write(render(tab_width, tab_fill, model))

def update_model(tab_width, tab_fill, model_name, view):
	with open(model_name, 'w') as model:
		model.write(desugar(tab_width, tab_fill, view))
