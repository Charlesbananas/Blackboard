import time
from tkinter import *
# from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw 
from handle_tools import *
from gizmos import gizmo # import PIL.ImageGrab as ImageGrab
from canvas import create_canvas # Use the reusable canvas factory from canvas.py
from tool_bar import change_brush_size, clear_canvas, save_image
from tkinter import colorchooser, messagebox

window = Tk()
window.title("Black_Board")

canvas = create_canvas(window, width=1200, height=1200, bg="black")

#painting to be replace with run_tool or an appropriate name
brush = paint_brush(canvas)
eraser_tool = eraser(canvas)
lasso = LassoTool(canvas)
text = TextTool(canvas)
shape = ShapeTool(canvas)

# Create the menu bar
menu_bar = Menu(window)

# Create the brush menu
brush_menu = Menu(menu_bar, tearoff=0)
brush_menu.add_command(label="Use Brush", command=brush.enable)
brush_menu.add_command(label="Brush Size", command= lambda : change_brush_size(brush=brush))

# Create the eraser menu
eraser_menu = Menu(menu_bar, tearoff=0)
eraser_menu.add_command(label="Use Eraser", command=eraser_tool.enable)
eraser_menu.add_command(label="Eraser Size", command=lambda : change_brush_size(brush=eraser_tool))

# Create the color menu
color_menu = Menu(menu_bar, tearoff=0)
color_menu.add_command(label="Select Drawing Color")

# Create the clear menu
clear_menu = Menu(menu_bar, tearoff=0)
clear_menu.add_command(label="Clear Canvas", command=lambda : clear_canvas(canvas))

# Create the tools menu
tool_menu = Menu(menu_bar, tearoff=0)
tool_menu.add_command(label="Select Text", command=text.enable)

# Create a dedicated nested submenu for geometric shapes
shape_submenu = Menu(tool_menu, tearoff=0)
shape_submenu.add_command(label="Oval", command=lambda: shape.enable("oval"))
shape_submenu.add_command(label="Rectangle", command=lambda: shape.enable("rectangle"))
shape_submenu.add_command(label="Line", command=lambda: shape.enable("line"))

# Add the shapes submenu as a cascade inside the tools menu
tool_menu.add_cascade(label="Select Shape...", menu=shape_submenu)

# Create Lasso/ Selection menu
Lasso_menu = Menu(menu_bar, tearoff=0)
Lasso_menu.add_command(label="Select Lasso",command=lasso.enable)

# Create the save menu
save_menu = Menu(menu_bar, tearoff=0)
save_menu.add_command(label="Save Drawing", command= lambda : save_image(window,canvas))

# Add the menus to the menu bar
menu_bar.add_cascade(label="Brush", menu=brush_menu)
menu_bar.add_cascade(label="Eraser", menu=eraser_menu)
menu_bar.add_cascade(label="Lasso", menu=Lasso_menu)
menu_bar.add_cascade(label="Color", menu=color_menu)
menu_bar.add_cascade(label="Tools", menu=tool_menu)
menu_bar.add_cascade(label="Clear", menu=clear_menu)
menu_bar.add_cascade(label="Save", menu=save_menu)

# Configure the menu bar
window.config(menu=menu_bar)

#register the gizmo drawing function to the canvas's mouse motion event

# from input_handler import Inputs
#custom input function might need it idk lol
# my_input = Inputs()

# Start with the brush selected
brush.enable()

# Start the Tk event loop
window.mainloop()
