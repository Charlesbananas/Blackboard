from tkinter import simpledialog
from tkinter import *
# import canvas

class Layers():
    def __init__(self,canvas,brush):
        self.current = "default"
        self.last = "last"
        self.canvas = canvas
        self.brush = brush
        self.layers = []
        self.layer_panels = []
        self.layers.append(self.current)

    def open_widget(self):
        self.widget = Tk()
        self.widget.attributes("-topmost",True)
        add_button = Button(self.widget,text="add",command=self.add_layer).pack(anchor="w") 
        if self.layer_panels:
            self.layer_panels = []
        for n in self.layers:
            self.layer_panels.append(self.layer_panel(self.widget,n))
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
        # self.widget.update()

    def get_current(self):
        return self.current
    
    def on_set_current(self,name):
        self.last = self.current
        self.current = name
        self.brush.set_tag(self.current)
        # print(self.current)
