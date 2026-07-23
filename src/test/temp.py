from PIL import Image

with Image.open("/Users/macbook/Desktop/Projects/Github/Blackboard/src/assets/paint.png") as img:
    _= img.resize((20,20))
    _.save("resize_paint.png")