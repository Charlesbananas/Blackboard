from tkinter import ROUND, simpledialog

class paint_brush:
    def __init__(self, canvas, on_new_item=None, tags=None):
        self.canvas = canvas
        self.brush_size = 1
        self.brush_color = "red"
        self.last_x, self.last_y = None, None
        self.tags = tags
        self.on_new_item = on_new_item
        self.current_stroke_items = [] # Track segments in this specific stroke
        
    def enable(self):
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def paint(self, event):
        if self.last_x and self.last_y:
            line_id = self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size, fill=self.brush_color,
                                    capstyle=ROUND, smooth=True, tags = self.tags)
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
    
    def set_color(self,color):
        print(color)
        self.brush_color = color
        self.enable()
    
    def set_tag(self,tag):
        print("tag: " + tag)
        self.tags = tag


class eraser:
    def __init__(self, canvas, on_new_item=None):
        self.canvas = canvas
        self.eraser_size = 10
        self.last_x, self.last_y = None, None
        self.on_new_item = on_new_item
        self.current_stroke_items = [] # Track segments in this specific stroke

    def enable(self):
        self.canvas.bind("<B1-Motion>", self.erase)
        self.canvas.bind("<Button-1>", self.reset)

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
        # this fix the issue where the eraser is acting like a black paint brush to an actual eraser 
        x, y = event.x, event.y
        r = self.eraser_size / 2
        items = self.canvas.find_overlapping(x - r, y - r, x + r, y + r)
        
        for item in items:
            if "gizmo" not in self.canvas.gettags(item):
                self.canvas.delete(item)

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
    def __init__(self, canvas, on_new_item=None):
        self.canvas = canvas
        self.on_new_item = on_new_item
        self.shape_type = "oval"
        self.color = "red"
        self.line_width = 3
        
        self.start_x = self.start_y = None
        self.last_x = self.last_y = None
        self.current_shape = None
        self.selected_shape = None
        
        # Flags
        self.is_resizing = False
        self.is_dragging = False
        
        # Overlay UI items
        self.hitbox_id = None
        self.bbox_id = None
        self.resize_handle = None
        self.delete_bg = None
        self.delete_text = None

    def set_shape_type(self, shape_type):
        if shape_type in ["rectangle", "oval", "line"]:
            self.shape_type = shape_type

    def enable(self, shape_type=None):
        if shape_type:
            self.set_shape_type(shape_type)
        self.deselect()
        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self.last_x, self.last_y = event.x, event.y
        clicked = self.canvas.find_withtag("current")
        
        if clicked:
            item = clicked[0]
            # 1. Clicked Delete Icon
            if item in (self.delete_bg, self.delete_text):
                self.delete_selected()
                return
            
            # 2. Clicked Resize Handle
            if item == self.resize_handle:
                self.is_resizing = True
                return
            
            # 3. Clicked Hitbox or Shape -> Select & Drag
            if item == self.hitbox_id or (item != self.bbox_id and "gizmo" not in self.canvas.gettags(item)):
                # If clicking directly on a new unselected shape
                if item != self.hitbox_id and item != self.selected_shape:
                    self.select_shape(item)
                self.is_dragging = True
                return

        # 4. Clicked outside -> Deselect & Draw new shape
        self.deselect()
        self.start_x, self.start_y = event.x, event.y

    def on_drag(self, event):
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        
        # Smooth Resizing
        if self.is_resizing and self.selected_shape:
            coords = self.canvas.coords(self.selected_shape)
            x1, y1 = coords[0], coords[1]
            self.canvas.coords(self.selected_shape, x1, y1, event.x, event.y)
            self.draw_controls()
            self.last_x, self.last_y = event.x, event.y
            return

        # Easy Free-Drag Moving
        if self.is_dragging and self.selected_shape:
            self.canvas.move(self.selected_shape, dx, dy)
            self.draw_controls()
            self.last_x, self.last_y = event.x, event.y
            return

        # New Shape Preview
        if self.start_x is not None:
            if self.current_shape:
                self.canvas.delete(self.current_shape)
            
            if self.shape_type == "rectangle":
                self.current_shape = self.canvas.create_rectangle(
                    self.start_x, self.start_y, event.x, event.y, outline=self.color, width=self.line_width
                )
            elif self.shape_type == "oval":
                self.current_shape = self.canvas.create_oval(
                    self.start_x, self.start_y, event.x, event.y, outline=self.color, width=self.line_width
                )
            elif self.shape_type == "line":
                self.current_shape = self.canvas.create_line(
                    self.start_x, self.start_y, event.x, event.y, fill=self.color, width=self.line_width
                )

    def on_release(self, event):
        if self.current_shape:
            shape_id = self.current_shape
            self.current_shape = None
            if self.on_new_item:
                self.on_new_item((shape_id,))
            self.select_shape(shape_id)
            
        self.is_resizing = False
        self.is_dragging = False
        self.start_x = self.start_y = None

    def select_shape(self, shape_id):
        self.deselect()
        self.selected_shape = shape_id
        self.draw_controls()

    def draw_controls(self):
        if not self.selected_shape:
            return
            
        x1, y1, x2, y2 = self.canvas.coords(self.selected_shape)
        # Add 6px padding to make the drag box feel spacious
        pad = 6
        x_min, x_max = min(x1, x2) - pad, max(x1, x2) + pad
        y_min, y_max = min(y1, y2) - pad, max(y1, y2) + pad
        
        self.clear_controls_only()

        # Invisible full-area click target (fill="" makes it transparent yet clickable)
        self.hitbox_id = self.canvas.create_rectangle(x_min, y_min, x_max, y_max, fill="", outline="")

        # Visible Bounding Frame
        self.bbox_id = self.canvas.create_rectangle(x_min, y_min, x_max, y_max, outline="cyan", dash=(3, 3))
        
        # Red 'X' Delete Icon
        btn_s = 8
        self.delete_bg = self.canvas.create_rectangle(
            x_max - btn_s, y_min - btn_s, x_max + btn_s, y_min + btn_s, fill="red", outline="white"
        )
        self.delete_text = self.canvas.create_text(
            x_max, y_min, text="×", fill="white", font=("Arial", 11, "bold")
        )
        
        # Bottom-Right Resize Circle
        r_s = 6
        self.resize_handle = self.canvas.create_oval(
            x_max - r_s, y_max - r_s, x_max + r_s, y_max + r_s, fill="white", outline="cyan", width=2
        )

    def delete_selected(self):
        if self.selected_shape:
            self.canvas.delete(self.selected_shape)
            self.deselect()

    def clear_controls_only(self):
        for item_id in (self.hitbox_id, self.bbox_id, self.delete_bg, self.delete_text, self.resize_handle):
            if item_id:
                self.canvas.delete(item_id)
        self.hitbox_id = self.bbox_id = self.delete_bg = self.delete_text = self.resize_handle = None

    def deselect(self):
        self.clear_controls_only()
        self.selected_shape = None