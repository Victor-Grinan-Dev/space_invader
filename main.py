import turtle
# import os
import math
import random

# set up the screen
win = turtle.Screen()
win.bgcolor("black")
win.title("Space Invaders")
win.setup(height=650, width=800)
# win.bgpic("bgspace.gif")
win.tracer(0)

# register shapes
# register_shape("space_ship.gif")
space_ship = ((0, 15), (-15, 0), (-18, 5), (-18, -5), (0, 0), (18, -5), (18, 5), (15, 0))
win.register_shape("space_ship", space_ship)

images = ["invader1.gif", "invader2.gif", "invader3.gif", "player1.gif", "player1.gif", "missile.gif"]
for img in images:
    win.register_shape(img)


# draw borders
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.pensize(3)
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.hideturtle()
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)

# score
score = 0

score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.hideturtle()
score_pen.penup()
score_pen.setposition(-290, 275)  # left up corner
score_string = f"Score: {score}"
score_pen.write(score_string, False, align="left", font=("Arial", 14, "normal"))

# create fake_players
player = turtle.Turtle()
player.hideturtle()
player.color("blue")
player.shape("turtle")
# fake_players.shape("space_ship.gif")
# fake_players.shapesize(0.01, 0.01)
player.setheading(90)
player.penup()
player.setposition(0, -250)
player_speed = 20
# x = fake_players.xcor()
player.speed = 15
player.showturtle()

# create new_enemy
enemy_speed = 0.5
enemies_amount = 20
enemies = []
for i in range(enemies_amount):
    enemy = turtle.Turtle()
    enemy.hideturtle()
    enemy.color("red")
    # new_enemy.shape("invaders")
    enemy.shape("turtle")
    enemy.setheading(270)
    # new_enemy.shapesize(0.01)
    enemy.penup()
    x = random.randint(-250, 250)
    y = random.randint(200, 250)
    enemy.setposition(x, y)
    enemy.speed(0)
    enemy.showturtle()
    enemies.append(enemy)

# create bullet
bullet = turtle.Turtle()
bullet.hideturtle()
bullet.color("yellow")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)

bullet_speed = 2
bullet_state = "ready"

# game over border_pen
game_over = False


def gameOver():
    global game_over
    game_over_string = f"GAME OVER!"  # \nYour Score: {score}
    score_pen.write(game_over_string, False, align="left", font=("Arial", 36, "normal"))
    game_over_pen = turtle.Turtle()
    game_over_pen.penup()
    game_over_pen.hideturtle()
    game_over_pen.color("white")
    game_over_pen.speed(0)
    game_over_pen.goto(0, 200)
    game_over = True


# move left
# def move_left():
#     global player_speed
#     player_speed *= -1  # turn value negative
#     move_player()
#
#
# # move right
# def move_right():
#     global player_speed
#     player_speed = abs(player_speed)  # turn value positive
#     move_player()
#
#
# def move_player():
#     x_ = fake_players.xcor()
#     x_ += player_speed
#     if x > 280:
#         fake_players.setx(x_)


# move left
def move_left():
    global player_speed
    player_speed *= -1


# move right
def move_right():
    global player_speed
    player_speed *= abs(player_speed)


# def player_move():
#     win.listen()
#
#     winonkey(move_left, "Left")
#     onkey(move_right, "Right")
#
#     player_x = player.xcor()
#     player_x += player.speed
#     if player_x > -280 and player_x > 280:
#         player.setx(player_x)


def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_x = player.xcor()
        bullet_y = player.ycor() + 10
        bullet.setposition(bullet_x, bullet_y)
        bullet.showturtle()
        bullet_state = "fired"


def is_collation(t1, t2):
    # teorema de Pitagoras
    # a = raiz_cuadrada(b**2 - c**2)
    distance_ = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance_ < 15:
        return True
    else:
        return False


def change_enemy_direction(enemy_speed):
    return enemy_speed * -1


def drop_enemy(enemy_):
    enemy_.sety(enemy_.ycor() - 20)


# keyboard binding
win.listen()
win.onkeypress(fire_bullet, "space")
win.onkeypress(move_left, "a")
win.onkey(move_right, "d")
# win.onkeypress(fire_bullet, "space")

# mainloop
while not game_over:
    win.update()

    # move new_enemy
    for enemy in enemies:
        x = enemy.xcor()
        x += enemy_speed
        enemy.setx(x)

        # check collation with wall
        # moving new_enemy down
        if x >= 280:
            for e in enemies:  # e for new_enemy
                drop_enemy(e)
            enemy_speed = change_enemy_direction(enemy_speed)
        if x <= -280:
            for e in enemies:
                drop_enemy(e)
            enemy_speed = change_enemy_direction(enemy_speed)

        # move bullet
        if bullet_state == "fired":
            y = bullet.ycor()
            y += bullet_speed
            bullet.sety(y)

        # check bullet in screen
        if bullet.ycor() >= 300:
            bullet.hideturtle()
            bullet_state = "ready"

        # check collation of bullet and new_enemy
        if is_collation(bullet, enemy):
            # reset the bullet
            bullet.hideturtle()
            bullet_state = "ready"
            bullet.setposition(0, -400)
            enemy.setposition(-200, 250)

            # update score
            score += 10
            score_pen.clear()
            score_string = f"Score: {score}"
            score_pen.write(score_string, False, align="left", font=("Arial", 14, "normal"))

        # check collation of fake_players and new_enemy
        if is_collation(player, enemy) or enemy.ycor() <= player.ycor():
            # reset the bullet
            player.hideturtle()
            enemy.hideturtle()
            gameOver()
            win.update()

win.exitonclick()
