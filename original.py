import turtle

width, height = 800, 600

win = turtle.Screen()
win.setup(width=width, height=height)
win.title("Space invaders")
win.bgcolor("black")
win.tracer(0)

# draw borders
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.pensize(3)
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
for side in range(4):
    border_pen.fd(width)
    border_pen.lt(90)
border_pen.hideturtle()

# create player
player = turtle.Turtle()
player.color("blue")
player.shape("turtle")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

player_speed = 15


def move_left():
    x = player.xcor()
    x -= player_speed
    player.setx(x)


def move_right():
    x = player.xcor()
    x += player_speed
    player.setx(x)


# key binding
win.listen()
turtle.onkey(move_left, "a")
turtle.onkey(move_right, "d")

while True:
    win.update()

# win.mainloop()
