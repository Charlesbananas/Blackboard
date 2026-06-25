from tkinter import ROUND

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