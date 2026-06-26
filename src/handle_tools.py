from tkinter import ROUND, simpledialog

class paint_brush():
    def __init__(self, canvas):
        self.canvas = canvas
        self.brush_size = 1
        self.brush_color = "red"
        self.last_x, self.last_y = None, None
        
    def enable(self):
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def paint(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size, fill=self.brush_color,
                                    capstyle=ROUND, smooth=True)
        self.last_x, self.last_y = event.x, event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def set_size(self,size):
        self.brush_size = size

    def get_size(self):
        return self.brush_size


class eraser:
    def __init__(self, canvas):
        self.canvas = canvas
        self.eraser_size = 10
        self.last_x, self.last_y = None, None

    def enable(self):
        self.canvas.bind("<B1-Motion>", self.erase)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def erase(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(
                self.last_x,
                self.last_y,
                event.x,
                event.y,
                width=self.eraser_size,
                fill="black",
                capstyle=ROUND,
                smooth=True
            )

        self.last_x, self.last_y = event.x, event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def set_size(self,size):
        self.eraser_size = size
    
    def get_size(self):
        return self.eraser_size
    
class TextTool:
    def __init__(self, canvas):
        self.canvas = canvas
        self.font_size = 16
        self.color = "white"

    def enable(self):
        #Bind single click to place text
        self.canvas.bind("<Button-1>", self.place_text)
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def place_text(self, event):
        #Open a simple Tkinter dialog box to grab text input
        user_text = simpledialog.askstring("Input", "Enter your text:")
        if user_text:
            self.canvas.create_text(
                event.x, event.y, 
                text=user_text, 
                fill=self.color, 
                font=("Arial", self.font_size),
                anchor="nw"
            )

class LassoTool:
    def __init__(self, canvas):
        self.canvas = canvas
        self.last_x, self.last_y = None, None
        self.current_lasso = None

    def enable(self):
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<B1-Motion>", self.draw_selection)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def click(self, event):
        self.last_x, self.last_y = event.x, event.y

    def draw_selection(self, event):
        if self.last_x and self.last_y:
            #Draw a dashed line showing the lasso selection boundary
            self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y,
                fill="gray", dash=(4, 4), width=1
            )
        self.last_x, self.last_y = event.x, event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None

class ShapeTool:
    def __init__(self, canvas):
        self.canvas = canvas
        self.start_x, self.start_y = None, None
        self.current_shape = None
        self.shape_type = "oval"  # Default shape
        self.color = "red"
        self.line_width = 3

    def set_shape_type(self, shape_type):
        if shape_type in ["rectangle", "oval", "line"]:
            self.shape_type = shape_type

    def enable(self, shape_type=None):
        if shape_type:
            self.set_shape_type(shape_type)
            
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<B1-Motion>", self.preview_shape)
        self.canvas.bind("<ButtonRelease-1>", self.finalize_shape)

    def click(self, event):
        self.start_x, self.start_y = event.x, event.y

    def preview_shape(self, event):
        if self.current_shape:
            self.canvas.delete(self.current_shape)
        
        if self.shape_type == "rectangle":
            self.current_shape = self.canvas.create_rectangle(
                self.start_x, self.start_y, event.x, event.y,
                outline=self.color, width=2
            )
        elif self.shape_type == "oval":
            self.current_shape = self.canvas.create_oval(
                self.start_x, self.start_y, event.x, event.y,
                outline=self.color, width=2
            )
        elif self.shape_type == "line":
            self.current_shape = self.canvas.create_line(
                self.start_x, self.start_y, event.x, event.y,
                fill=self.color, width=self.line_width, capstyle=ROUND
            )

    def finalize_shape(self, event):
        self.current_shape = None