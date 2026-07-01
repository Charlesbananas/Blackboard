from tkinter import ROUND, simpledialog

class paint_brush():
    def __init__(self, canvas, on_new_item=None):
        self.canvas = canvas
        self.brush_size = 1
        self.brush_color = "red"
        self.last_x, self.last_y = None, None
        self.on_new_item = on_new_item
        self.current_stroke_items = [] # Track segments in this specific stroke
        
    def enable(self):
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def paint(self, event):
        if self.last_x and self.last_y:
            line_id = self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size, fill=self.brush_color,
                                    capstyle=ROUND, smooth=True)
            self.current_stroke_items.append(line_id)
        self.last_x, self.last_y = event.x, event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None
        # When user releases mouse, send the whole line path to the undo stack
        if self.current_stroke_items and self.on_new_item:
            self.on_new_item(tuple(self.current_stroke_items))
        self.current_stroke_items = []

    def set_size(self,size):
        self.brush_size = size

    def get_size(self):
        return self.brush_size


class eraser:
    def __init__(self, canvas, on_new_item=None):
        self.canvas = canvas
        self.eraser_size = 10
        self.last_x, self.last_y = None, None
        self.on_new_item = on_new_item
        self.current_stroke_items = [] # Track segments in this specific stroke

    def enable(self):
        self.canvas.bind("<B1-Motion>", self.erase)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def erase(self, event):
        if self.last_x and self.last_y:
            line_id = self.canvas.create_line(
                self.last_x,
                self.last_y,
                event.x,
                event.y,
                width=self.eraser_size,
                fill="black",
                capstyle=ROUND,
                smooth=True
            )
            self.current_stroke_items.append(line_id)
        self.last_x, self.last_y = event.x, event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None
        if self.current_stroke_items and self.on_new_item:
            self.on_new_item(tuple(self.current_stroke_items))
        self.current_stroke_items = []

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
        self.selected_items = []
        self.selection_line = None
        self.points = [] # Holds all coordinates along the custom path

    def enable(self):
        # Bind freehand path generation
        self.canvas.bind("<Button-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.draw_selection)
        self.canvas.bind("<ButtonRelease-1>", self.end_selection)
        
        # Keep keyboard deletion focus
        self.canvas.focus_set()
        self.canvas.bind("<Delete>", self.delete_selected)

    def start_selection(self, event):
        self.clear_selection_visuals()
        self.last_x, self.last_y = event.x, event.y
        self.points = [(event.x, event.y)]

    def draw_selection(self, event):
        # Append the new mouse location to our trail history
        self.points.append((event.x, event.y))
        
        # Dynamically draw the freehand trail as a dashed line
        if len(self.points) > 1:
            if self.selection_line:
                self.canvas.delete(self.selection_line)
                
            # Flatten the points array [(x1,y1), (x2,y2)] -> [x1, y1, x2, y2]
            flat_points = [coord for pt in self.points for coord in pt]
            self.selection_line = self.canvas.create_line(
                flat_points, fill="cyan", dash=(4, 4), smooth=True
            )

    def end_selection(self, event):
        if not self.points or len(self.points) < 2:
            return

        # Automatically connect the last point back to the starting point to close the lasso loop
        self.points.append(self.points[0])
        flat_points = [coord for pt in self.points for coord in pt]
        
        # Redraw closed path loop
        if self.selection_line:
            self.canvas.delete(self.selection_line)
        self.selection_line = self.canvas.create_line(
            flat_points, fill="lime", dash=(4, 4), smooth=True
            )

        # Calculate the bounding box of your freestyle path to gather internal objects
        x_coords = [p[0] for p in self.points]
        y_coords = [p[1] for p in self.points]
        x1, y1 = min(x_coords), min(y_coords)
        x2, y2 = max(x_coords), max(y_coords)

        # Find everything touching or inside the region boundaries
        self.selected_items = list(self.canvas.find_overlapping(x1, y1, x2, y2))
        
        # Strip the selection lines out of the payload array
        if self.selection_line in self.selected_items:
            self.selected_items.remove(self.selection_line)

        if self.selected_items:
            # Rebind drag functions to MOVE mode instead of DRAW mode
            self.canvas.bind("<Button-1>", self.start_move)
            self.canvas.bind("<B1-Motion>", self.move_items)
            self.canvas.bind("<ButtonRelease-1>", self.end_move)
        else:
            self.clear_selection_visuals()

    def start_move(self, event):
        self.last_x, self.last_y = event.x, event.y

    def move_items(self, event):
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        
        # Translate the enclosed lines/shapes
        for item in self.selected_items:
            self.canvas.move(item, dx, dy)
            
        # Move the freestyle green layout overlay with the items
        if self.selection_line:
            self.canvas.move(self.selection_line, dx, dy)
            
        self.last_x, self.last_y = event.x, event.y

    def end_move(self, event):
        # Put the tool back in selection mode for the next action
        self.enable()

    def delete_selected(self, event=None):
        """Removes all objects inside your drawn path loop"""
        for item in self.selected_items:
            self.canvas.delete(item)
        self.clear_selection_visuals()
        self.enable()

    def clear_selection_visuals(self):
        if self.selection_line:
            self.canvas.delete(self.selection_line)
            self.selection_line = None
        self.selected_items = []
        self.points = []

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