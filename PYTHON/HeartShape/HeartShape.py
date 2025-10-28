import turtle

t = turtle.Turtle()
t.color("red")
t.begin_fill()
t.left(140)
t.forward(180)
for i in range(200):
    t.right(1)
    t.forward(2)
t.left(120)
for i in range(200):
    t.right(1)
    t.forward(2)
t.forward(180)
t.end_fill()
turtle.done()
