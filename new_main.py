import turtle
import math
import time

width, height = 800, 600
hell = 1000, 1000

win = turtle.Screen()
win.setup(width=width, height=height)
win.title("Space invaders")
win.bgcolor("black")
win.tracer(0)
win.bgpic("bgspace.gif")

# images
images = ["invader1.gif", "invader2.gif", "invader3.gif", "missile.gif", "player1.gif", "invader1.gif", "explosion.gif"]
for img in images:
    turtle.register_shape(img)

# game
game_on = True

# level
level = 1
level_pen = turtle.Turtle()
level_pen.speed(0)
level_pen.color("white")
level_pen.shape("turtle")
level_pen.penup()
level_pen.setposition(-350, 255)
level_font = ("Arial", 12, "normal")
level_text = f"Level: {level}"
level_pen.write(level_text, align="center", font=level_font)
level_pen.hideturtle()

# borders
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.pensize(3)
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# create fake_players
fake_players = []
lives = 3
x = 350
y = 200

for _ in range(lives):
    fake_player = turtle.Turtle()
    fake_players.append(fake_player)

for fake_player in fake_players:
    fake_player.color("blue")
    fake_player.shape("turtle")
    fake_player.penup()
    fake_player.speed(0)

    fake_player.setheading(180)
    fake_player.setposition(x, y)
    y += 30

fake_player_index = 2
fake_player_on_position = False

player = turtle.Turtle()
player.hideturtle()
player_position = (0, -250)
player.color("blue")
player.shape("turtle")
player.penup()
player.speed(0)
player_speed = 15
player.setheading(90)
player.setposition(player_position)

# score
score = 0
score_pen = turtle.Turtle()
score_pen.penup()
score_pen.speed(0)
score_pen.color("white")
score_pen.setposition(-350, 155)
score_string = f"Score: {score}"
score_font = ("Arial", 12, "normal")
score_pen.hideturtle()
score_pen.write(score_string, align="center", font=score_font)

# create missile
missile = turtle.Turtle()
missile.color("yellow")
missile.shape("triangle")
missile.shape("missile.gif")
missile.penup()
missile.speed(0)
missile.setheading(90)
missile.shapesize(0.5, 0.5)
missile.hideturtle()
missile_speed = 2
missile_state = "ready"
missile_in_game = True

# create new_enemy
num_of_enemies = 5
enemies = []
enemy_speed = 0.1


def reset_enemies():
    global enemy_speed, num_of_enemies
    enemy_start_x = -200
    enemy_start_y = 250
    enemy_number = 0

    num_of_enemies += 10
    enemy_speed += 0.2

    for _ in range(num_of_enemies):
        enemies.append(turtle.Turtle())

    for enemy_ in enemies:
        enemy_.color("red")
        enemy_.shape("turtle")
        enemy_.setheading(270)
        enemy_.penup()
        enemy_.speed(0)

        # positioning
        _enemy_x = enemy_start_x + (40 * enemy_number)
        _enemy_y = enemy_start_y
        enemy_.setposition(_enemy_x, _enemy_y)
        enemy_number += 1
        if enemy_number == 10:
            enemy_start_y -= 40
            enemy_number = 0


# move
def move_left():
    x_ = player.xcor()
    x_ -= player_speed
    if x_ < -280:
        x_ = -280
    player.setx(x_)


def move_right():
    x_ = player.xcor()
    x_ += player_speed
    if x_ > 280:
        x_ = 280
    player.setx(x_)


def fire():
    global missile_state
    if missile_state == "ready":
        posx = player.xcor()
        posy = player.ycor() + 10
        missile.setposition(posx, posy)
        missile.showturtle()
        missile_state = "fired"


def is_collision(t1, t2):
    distance_ = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance_ < 15:
        return True
    else:
        return False


# key binding
win.listen()
win.onkeypress(move_left, "a")
win.onkeypress(move_left, "Left")
win.onkeypress(move_right, "d")
win.onkeypress(move_right, "Right")
win.onkey(fire, "space")
win.onkey(fire, "Up")
win.onkey(fire, "w")

# todo: instead of creating many players just make them grafic and just one player
while game_on:

    win.update()

    if not fake_player_on_position:
        fplayer = fake_players[fake_player_index]
        fplayer.setheading(player.towards(player_position))
        while fplayer.xcor() > player_position[0] or fplayer.ycor() > player_position[1]:
            fplayer.fd(3)
            win.update()
        fake_player_on_position = True
        player.showturtle()
        fplayer.hideturtle()
        fplayer.goto(hell)

    # move the new_enemy
    for enemy in enemies:
        x = enemy.xcor()
        x += enemy_speed
        enemy.setx(x)

        # reach border move down and back
        if enemy.xcor() > 280 or enemy.xcor() < -280:
            for e in enemies:
                y = e.ycor()
                y -= 50
                e.sety(y)
            enemy_speed *= -1

        # collision checks
        # missile-new_enemy collision
        if is_collision(missile, enemy):
            if missile_in_game:
                missile.hideturtle()
                missile_in_game = False
                missile.goto(hell)
                missile_state = "ready"
                enemy.hideturtle()
                enemies.remove(enemy)
                enemy.goto(hell)
                enemy.showturtle()
                score += 10
                score_pen.clear()
                score_string = f"Score: {score}"
                score_pen.write(score_string, align="center", font=score_font)

        # enemy-player collision
        if is_collision(enemy, player):
            player.shape("explosion.gif")
            win.update()
            time.sleep(1)
            player.goto(hell)
            player_on_position = False
            if len(fake_players) > 0:
                fake_players.remove(player)
                fake_player_index -= 1
                player = fake_players[fake_player_index]

                # clear the remaining enemies
                for e in enemies:
                    e.goto(hell)
                enemies.clear()

                reset_enemies()
                # bind_keys()

            else:
                game_over = turtle.Turtle()
                game_over.hideturtle()
                game_over.color("white")
                game_over_text = "GAME OVER!"
                game_over.write(game_over_text, align="center", font=level_font)
                win.update()
                game_on = False

    # missile behavior
    if missile_state == "fired":
        missile.fd(missile_speed)
    if missile.ycor() > 300:
        missile.hideturtle()
        missile_in_game = True
        missile_state = "ready"

    if not enemies:
        level += 1
        level_pen.clear()
        level_pen.write(f"Level: {level}", align="center", font=level_font)

        # create enemies
        reset_enemies()
    win.update()
win.mainloop()
