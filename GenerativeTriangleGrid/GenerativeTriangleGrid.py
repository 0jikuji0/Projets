from PIL import Image, ImageDraw
import random

w,h = 400,400
img = Image.new("RGB",(w,h),"black")
draw = ImageDraw.Draw(img)

for i in range(1000):
    x1,y1 = random.randint(0,w), random.randint(0,h)
    x2,y2 = x1 + random.randint(-30,30), y1 + random.randint(-30,30)
    x3,y3 = x1 + random.randint(-30,30), y1 + random.randint(-30,30)
    color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    draw.polygon([(x1,y1),(x2,y2),(x3,y3)], fill=color)
img.show()
