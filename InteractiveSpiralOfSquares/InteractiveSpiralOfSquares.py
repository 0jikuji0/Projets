import turtle, colorsys
t=turtle.Turtle()
t.speed(0)
turtle.bgcolor('black')
turtle.colormode(255)

for i in range(120):
    color=colorsys.hsv_to_rgb(i/120,1,1)
    t.pencolor(int(color[0]*255),int(color[1]*255),int(color[2]*255))
    for j in range(4):
        t.forward(i*2)
        t.right(90)
    t.right(10)
turtle.done()

