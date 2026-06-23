from PIL import Image

def select_brush():
    pass
def change_brush_size():
    pass
def select_eraser():
    pass
def change_eraser_size():
    pass
def select_brush_color():
    pass
def clear_canvas():
    pass
def Lasso():
    pass
def select_shape():
    pass
def save_image( window, canvas):
    print("Save Command called")
     # 1. Update tasks to ensure full render
    window.update_idletasks()
    # 2. Save canvas content to EPS
    canvas.postscript(file="drawing.eps", colormode='color')
    # 3. Open with Pillow and convert to PNG
    img = Image.open("drawing.eps")
    img.save("drawing.png", "png")
    pass