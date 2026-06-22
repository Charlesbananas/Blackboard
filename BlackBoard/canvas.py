import tkinter as tk

def create_canvas(parent, width=1200, height=1200, bg='black', **pack_opts):
	"""Create and return a Canvas widget attached to the given parent.

	This function does not create a new Tk root or call `mainloop()` so it
	can be embedded into other modules (e.g. `main.py`).
	"""
	canvas = tk.Canvas(parent, width=width, height=height, bg=bg)
	# default packing options; caller can override via pack_opts
	default_pack = dict(anchor=tk.CENTER, expand=True)
	default_pack.update(pack_opts)
	canvas.pack(**default_pack)
	# canvas.create_line(50, 50, 350, 250, fill="blue", width=3)
	return canvas