from PIL import Image
from tkinter import * 
import canvas

#we should change it so that it's a fixed slider on the menu for any tool for now it's a wiget 
#oki doki, we also should only start focusing on GUI, once all the function are complete 
#and most imopartantly working.
def change_brush_size(brush):
    widget = Tk()
    widget.title = "set size"
    scale = Scale(widget,orient="horizontal")
    scale.set(brush.get_size())
    def test(value):
        brush.set_size(scale.get())
    scale.config(command=test)
    scale.pack()
    widget.mainloop()
    pass
def clear_canvas(canvas_widget):
    canvas_widget.delete('all')
    pass
def save_image( window, canvas):# chanage
    print("Save Command called")
     # 1. Update tasks to ensure full render
    window.update_idletasks()
    # 2. Save canvas content to EPS
    canvas.postscript(file="drawing.eps", colormode='color')
    # 3. Open with Pillow and convert to PNG
    img = Image.open("drawing.eps")
    img.save("drawing.png", "png")
    pass