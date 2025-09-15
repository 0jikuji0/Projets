import turtle, colorsys
t = turtle.Turtle()
turtle.bgcolor("black")
t.speed(0)
colors = [colorsys.hsv_to_rgb(x/36, 1, 1) for x in range(36)]

for x in range(360):
    t.color(colors[x])
    t.circle(100)
    t.left(10)

turtle.done()
