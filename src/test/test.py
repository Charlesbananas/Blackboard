from tkinter import *

def test():
    root = Tk()
    root.title = "TEST"
    root.geometry("700x400")

    tool_menu = Menu(root,tearoff=0)
    def null_command(): pass

    
    
    add_menu_item(tool_menu,"item",null_command)
    # add_scale_slider(tool_menu)
    frame = Frame(root,bg="grey")
    frame.pack(fill="y",side="right")
    


    add_scale_slider(frame)
    
    create_floating_window(root,label_text="scale")
    root.config(menu=tool_menu)

    root.mainloop()

def add_menu_item(parent,_label,_command):
    variable_menu = Menu(parent,tearoff=0)
    variable_menu.add_command(label=_label,command=_command)
    parent.add_cascade(label=_label,menu=variable_menu)

def add_scale_slider(parent):
    scale = Scale(parent,orient="horizontal")
    scale.pack()

def create_floating_window(root,label_text):
    draggable = DraggableFrame(root,width=100,height=100,relief="raised")
    draggable.place(x=0,y=0)
    label = Label(draggable,text=label_text)
    label.pack()
    label.bind("<Button-1>",draggable.on_start)
    label.bind("<B1-Motion>",draggable.on_drag)
    scale = Scale (draggable,orient="horizontal")
    scale.pack()
    


class DraggableFrame(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        # Bind mouse events for dragging
        self.bind("<Button-1>", self.on_start)
        self.bind("<B1-Motion>", self.on_drag)
        
        self.start_x = 0
        self.start_y = 0

    def on_start(self, event):
        # Store relative click coordinates inside the frame
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        # Calculate new absolute coordinates on the window
        deltax = event.x - self.start_x
        deltay = event.y - self.start_y
        
        new_x = self.winfo_x() + deltax
        new_y = self.winfo_y() + deltay
        
        # Reposition the frame
        self.place(x=new_x, y=new_y)
test()

tkInstance = Tk()
button = Button(tkInstance)

for option in button.configure():
    print(option)