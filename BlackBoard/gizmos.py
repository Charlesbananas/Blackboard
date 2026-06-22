class gizmo():
    def __init__(self, canvas):
        self.canvas = canvas
        self.size = 10
        self.color = "white"
        self.canvas.bind("<Motion>", self.draw)

    def draw(self, event):
        x, y = event.x, event.y
        # Clear the previous gizmo
        self.canvas.delete("gizmo")
        self.canvas.create_line(x - self.size, y, x + self.size, y, fill=self.color, width=1, tags="gizmo", dash=(1,1))
        self.canvas.create_line(x, y - self.size, x, y + self.size, fill=self.color, width=1, tags="gizmo", dash=(1,1))
        self.last_x, self.last_y = None, None   

