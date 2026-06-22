import time
from tkinter import *
# from tkinter import filedialog
# from PIL import Image, ImageTk, ImageDraw
from handle_paint import *
from gizmos import gizmo
# import PIL.ImageGrab as ImageGrab

from tkinter import colorchooser, messagebox

window = Tk()
window.title("Black_Board")
from tool_bar import select_brush, change_brush_size, select_eraser, change_eraser_size, select_brush_color, clear_canvas, save_image

# Create the menu bar
menu_bar = Menu(window)

# Create the brush menu
brush_menu = Menu(menu_bar, tearoff=0)
brush_menu.add_command(label="Select Brush", command=select_brush)
brush_menu.add_command(label="Brush Size", command=change_brush_size)

# Create the eraser menu
eraser_menu = Menu(menu_bar, tearoff=0)
eraser_menu.add_command(label="Select Eraser", command=select_eraser)
eraser_menu.add_command(label="Eraser Size", command=change_eraser_size)

# Create the color menu
color_menu = Menu(menu_bar, tearoff=0)
color_menu.add_command(label="Select Drawing Color", command=select_brush_color)

# Create the clear menu
clear_menu = Menu(menu_bar, tearoff=0)
clear_menu.add_command(label="Clear Canvas", command=clear_canvas)

# Create the save menu
save_menu = Menu(menu_bar, tearoff=0)
save_menu.add_command(label="Save Drawing", command=save_image)

# Add the menus to the menu bar
menu_bar.add_cascade(label="Brush", menu=brush_menu)
menu_bar.add_cascade(label="Eraser", menu=eraser_menu)
menu_bar.add_cascade(label="Color", menu=color_menu)
menu_bar.add_cascade(label="Clear", menu=clear_menu)
menu_bar.add_cascade(label="Save", menu=save_menu)

# Configure the menu bar
window.config(menu=menu_bar)

# Use the reusable canvas factory from canvas.py
from canvas import create_canvas

canvas = create_canvas(window, width=1200, height=500, bg="black")

#register the gizmo drawing function to the canvas's mouse motion event
paint_brush(canvas)
gizmo(canvas)
# Start the Tk event loop
window.mainloop()

# print(window.winfo_width())