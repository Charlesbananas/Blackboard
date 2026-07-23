from tkinter import *
from PIL import Image,ImageTk
from tkinter import simpledialog

def app():
    root = Tk()
    root.title = "TEST"
    root.geometry("700x400")
    canvas = Canvas(root,width=600,height=300,bg="white")
    line = canvas.create_line(0,0,100,100,fill="red",tags="line")
    canvas.pack()

    # current_layer = Layer(canvas,name = "Layer 1")

    def test(event):
        print(event.keysym)
        print("Key pressed")
        canvas.itemconfig("line",state="hidden")
    
    brush(canvas,"line")

    root.bind("<space>",test)

    root.mainloop()

class brush:
    def __init__(self,canvas,tags):
            self.canvas = canvas
            self.brush_size=1
            self.brush_color = "red"
            self.last_x, self.last_y = None, None
            self.current_stroke_items=[]
            self.tags = tags
            self.canvas.bind("<B1-Motion>",self.paint)
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
        # if self.current_stroke_items and self.on_new_item:
        #     # for _ in self.on_new_item:
        #         # _(tuple(self.current_stroke_items))
        #     self.on_new_item(self.current_stroke_items)
                # print(_)
        self.current_stroke_items = []

        

app()