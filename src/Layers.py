from tkinter import simpledialog
from tkinter import *
from handle_tools import paint_brush
# import canvas

class Layers():
    def __init__(self,canvas,brush):
        self.canvas = canvas
        self.brush = brush
        self.layers = []
        self.layer_panels = []
        self.layers.append("default")
        self.current = None
        self.last = None

    def open_widget(self):
        self.widget = Tk()
        self.widget.attributes("-topmost",True)
        add_button = Button(self.widget,text="add",command=self.add_layer).pack(anchor="w") 
        if self.layer_panels:
            self.layer_panels = []
        for n in self.layers:
            self.layer_panels.append(self.layer_panel(self.widget,n))
        self.current= StringVar(value="default")
        self.last = self.current.get()
        self.widget.mainloop()
        
    def raise_layer(self,layer,frame):
        index = self.layers.index(layer)
        if index == 0:
            pass
        else:
            self.canvas.tag_raise(layer)#apply on canvas object
            temp = self.layers[index-1]
            self.layers[index-1] = self.layers[index]
            self.layers[index] = temp
            if self.layer_panels:
                frame.pack(before=self.layer_panels[index-1])
                tempFrame = self.layer_panels[index-1]
                self.layer_panels[index-1]=self.layer_panels[index]
                self.layer_panels[index]=tempFrame

    def lower_layer(self,layer,frame):
        index = self.layers.index(layer)
        if index == len(self.layers)-1:
            pass
        else:
            self.canvas.tag_lower(layer)
            temp = self.layers[index+1]
            self.layers[index+1] = self.layers[index]
            self.layers[index] = temp
            if self.layer_panels:
                frame.pack(after=self.layer_panels[index+1])
                tempFrame = self.layer_panels[index+1]
                self.layer_panels[index+1]=self.layer_panels[index]
                self.layer_panels[index]=tempFrame

    def delete_layer(self,layer,frame):
        self.layers.remove(layer)
        if self.layer_panels:
            self.layer_panels.remove(frame)
            frame.destroy()
        self.canvas.delete(layer)
        self.widget.update()
    
    def layer_panel(self,parent,_name):
        frame = Frame(parent)
        radiobutton = Radiobutton(frame,variable=self.current,value=_name,command= lambda: self.on_set_current(_name)).grid(column=0,row=0)
        label = Label(frame,text=_name).grid(column=1,row=0)
        raise_button = Button(frame,text="raise",command=lambda:self.raise_layer(_name,frame)).grid(column=2,row=0)
        lower_button = Button(frame,text="lower",command=lambda:self.lower_layer(_name,frame)).grid(column=3,row=0)
        delete_button = Button(frame,text="delete",command=lambda:self.delete_layer(_name,frame)).grid(column=4,row=0)
        frame.pack()
        return frame
    
    def add_layer(self):
        layer_name = simpledialog.askstring("Layer","enter layer name",parent=self.widget)
        if layer_name in self.layers:
            pass
        else:
            self.layers.append(layer_name)
            self.layer_panels.append(self.layer_panel(self.widget,layer_name))
            self.on_set_current(layer_name)
        # self.widget.update()

    def get_current(self):
        return self.current.get()
    
    def on_set_current(self,name):
        self.last = self.current.get()
        self.current.set(name)
        self.brush.set_tag(self.current.get())
        # print(self.current)

def test():
    augustine = Tk()
    canvas = Canvas(augustine,width=100,height=100).pack()
    brush = paint_brush(canvas=canvas)
    layer = Layers(canvas=canvas,brush=brush)

    button = Button(augustine,text="open",command=layer.open_widget).pack()

    augustine.mainloop()

test()