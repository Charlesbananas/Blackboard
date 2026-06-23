from tkinter import ROUND

class paint_brush():
    def __init__(self, canvas):
        self.canvas = canvas
        self.brush_size = 1
        self.brush_color = "red"
        self.last_x, self.last_y = None, None
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

class eraser():
    def __init__(self):
        pass
    def erase():
        pass
    def reset():
        pass