import turtle, math, colorsys

t=turtle.Turtle()
turtle.bgcolor("black")
t.speed(0)
turtle.colormode(255)

for i in range(360):
    c=colorsys.hsv_to_rgb(i/360,1,1)
    t.pencolor(int(c[0]*255),int(c[1]*255),int(c[2]*255))
    t.penup()
    r = i * 0,5
    t.goto(r * math.cos(i * math.pi / 30), r * math.sin(i * math.pi / 30))    
    t.pendown() 
    t.dot(i%10+5)

turtle.done()