from PIL import Image
from tkinter import * 
from tkinter import simpledialog
from tkinter import colorchooser
# from main import layer_window
# import canvas

#we should change it so that it's a fixed slider on the menu for any tool for now it's a wiget 
#oki doki, we also should only start focusing on GUI, once all the function are complete 
#and most imopartantly working.
def change_brush_size(brush):
    widget = Tk()
    widget.title = "set size"
    scale = Scale(widget,orient="horizontal")
    scale.set(brush.get_size())
    def test(value):
        brush.set_size(scale.get())
    scale.config(command=test)
    scale.pack()
    widget.mainloop()
    pass
def clear_canvas(canvas_widget):
    canvas_widget.delete('all')
    pass

undo_stack = []
redo_stack = []

def add_to_undo(item_tuple):
    """Call this whenever a tool finishes drawing a line, text, or shape"""
    undo_stack.append(item_tuple)
    redo_stack.clear() # Clear redo history on a brand new action

def undo_action(canvas_widget, event=None): # <-- Added event=None
    if undo_stack:
        action_item = undo_stack.pop()
        redo_stack.append(action_item)
        
        # Hide the canvas components belonging to this action group
        for item_id in action_item:
            canvas_widget.itemconfig(item_id, state='hidden')

def redo_action(canvas_widget, event=None): # <-- Added event=None
    if redo_stack:
        action_item = redo_stack.pop()
        undo_stack.append(action_item)
        
        # Make the canvas components visible again
        for item_id in action_item:
            canvas_widget.itemconfig(item_id, state='normal')

def save_image( window, canvas):# chanage
    print("Save Command called")
     # 1. Update tasks to ensure full render
    window.update_idletasks()
    # 2. Save canvas content to EPS
    canvas.postscript(file="drawing.eps", colormode='color')
    # 3. Open with Pillow and convert to PNG
    img = Image.open("drawing.eps")
    img.save("drawing.png", "png")
    pass

# def open_layer_window():
#     layer_window.open_window()

def select_color(brush):
    color = colorchooser.askcolor()
    brush.set_color(color[1])