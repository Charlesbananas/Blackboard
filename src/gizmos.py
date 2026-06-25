
class gizmo():
    def __init__(self, canvas):
        self.canvas = canvas
        self.size = 10
        self.color = "white"
        self.canvas.bind("<Motion>",self.draw)
        # self.canvas.bind("<B1-Motion>", self.draw)

    def draw(self, event):
        x, y = event.x, event.y
        x1,y1 = event.x - self.size/2,event.y + self.size/2
        x2,y2 = event.x + self.size/2,event.y - self.size/2
        # Clear the previous gizmo
        self.canvas.delete("gizmo")
        self.canvas.create_oval(x1,y1,x2,y2,fill="",outline=self.color,width=1,tag="gizmo",dash=(1,1))
        # self.canvas.create_line(x - self.size, y, x + self.size, y, fill=self.color, width=1, tags="gizmo", dash=(1,1))
        # self.canvas.create_line(x, y - self.size, x, y + self.size, fill=self.color, width=1, tags="gizmo", dash=(1,1))
        self.last_x, self.last_y = None, None   

    def set_size(self,size):
        self.size = size

