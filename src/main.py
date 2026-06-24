import time
from tkinter import *
# from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw 
from handle_tools import *
from gizmos import gizmo # import PIL.ImageGrab as ImageGrab
from canvas import create_canvas # Use the reusable canvas factory from canvas.py
from tool_bar import change_brush_size, change_eraser_size, select_brush_color, clear_canvas, save_image
from tkinter import colorchooser, messagebox

window = Tk()
window.title("Black_Board")

canvas = create_canvas(window, width=2000, height=2000, bg="black")

#painting to be replace with run_tool or an appropriate name
brush = paint_brush(canvas)
eraser_tool = eraser(canvas)

# Create the menu bar
menu_bar = Menu(window)

# Create the brush menu
brush_menu = Menu(menu_bar, tearoff=0)
brush_menu.add_command(label="Use Brush", command=brush.enable)
brush_menu.add_command(label="Brush Size", command=change_brush_size)

# Create the eraser menu
eraser_menu = Menu(menu_bar, tearoff=0)
eraser_menu.add_command(label="Use Eraser", command=eraser_tool.enable)
eraser_menu.add_command(label="Eraser Size", command=change_eraser_size)

# Create the color menu
color_menu = Menu(menu_bar, tearoff=0)
color_menu.add_command(label="Select Drawing Color", command=select_brush_color)

# Create the clear menu
clear_menu = Menu(menu_bar, tearoff=0)
clear_menu.add_command(label="Clear Canvas", command=clear_canvas)


# Create the save menu
save_menu = Menu(menu_bar, tearoff=0)
save_menu.add_command(label="Save Drawing", command= lambda : save_image(window,canvas))


# Add the menus to the menu bar
menu_bar.add_cascade(label="Brush", menu=brush_menu)
menu_bar.add_cascade(label="Eraser", menu=eraser_menu)
menu_bar.add_cascade(label="Color", menu=color_menu)
menu_bar.add_cascade(label="Clear", menu=clear_menu)
menu_bar.add_cascade(label="Save", menu=save_menu)

# Configure the menu bar
window.config(menu=menu_bar)

#register the gizmo drawing function to the canvas's mouse motion event
gizmo(canvas)

# Start with the brush selected
brush.enable()

# Start the Tk event loop
window.mainloop()
