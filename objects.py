import turtle
import math


class Sprite(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.penup()


class Player(Sprite):
    player_speed = 15
    player_position = (0, -250)

    missile_speed = 2
    missile_state = "ready"
    missile_in_game = True

    def __init__(self):
        super().__init__()
        # self.hideturtle()

        self.color("blue")
        self.shape("turtle")
        self.setheading(90)
        self.setposition(self.player_position)
        self.speed(0)

        self.missile = Sprite()
        self.missile.hideturtle()
        self.missile.penup()
        self.missile.speed(0)
        self.missile.shapesize(0.5, 0.5)
        self.missile_state = "ready"
        self.missile.color("yellow")
        self.missile.shape("triangle")
        self.missile.shape("missile.gif")

    def move_left(self):
        x_ = self.xcor()
        x_ -= self.player_speed
        if x_ < -280:
            x_ = -280
        self.setx(x_)

    def move_right(self):
        x_ = self.xcor()
        x_ += self.player_speed
        if x_ > 280:
            x_ = 280
        self.setx(x_)

    def fire(self):
        self.missile.setheading(90)  # in case is broken code
        if self.missile_state == "ready":
            posx = self.xcor()
            posy = self.ycor() + 10
            self.missile.setposition(posx, posy)
            self.missile.showturtle()
            self.missile_state = "fired"


class Enemy:
    amount = 0
    all_enemies = []
    speed = 0.1
    start_x = -200
    start_y = 250
    tag_number = 0

    def __init__(self):
        super().__init__()

        self.reset_enemies()

    @staticmethod
    def enemy_object():
        object_ = turtle.Turtle()
        object_.penup()
        object_.color("red")
        object_.shape("turtle")
        object_.setheading(270)
        return object_

    def reset_enemies(self):  # todo: not working
        self.amount += 10
        self.speed += 0.2

        for _ in range(self.amount):
            self.all_enemies.append(self.enemy_object())

        for enemy_ in self.all_enemies:
            # positioning
            enemy_x = self.start_x + (40 * self.tag_number)
            enemy_y = self.start_y
            enemy_.setposition(enemy_x, enemy_y)
            self.tag_number += 1
            if self.tag_number == 10:
                self.start_y -= 40
                self.tag_number = 0

    def move(self):
        for element in self.all_enemies:
            x = element.xcor()
            x += self.speed
            element.setx(x)

            # reach border move down and back
            if element.xcor() > 280 or element.xcor() < -280:
                for e in self.all_enemies:
                    y = e.ycor()
                    y -= 50
                    e.sety(y)
                self.speed *= -1


class Game:
    screen = turtle.Screen()

    width, height = 800, 600
    hell = 1000, 1000

    images = ["invader1.gif", "invader2.gif", "invader3.gif", "missile.gif", "player1.gif", "invader1.gif",
              "explosion.gif"]
    for img in images:
        turtle.register_shape(img)

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

    def __init__(self):
        # super().__init__()
        # self.screen.tracer(0)
        self.screen.setup(width=self.width, height=self.height)
        self.screen.title("Space invaders")
        self.screen.bgcolor("black")
        self.screen.bgpic("bgspace.gif")
        # self.screen.listen()

        self.game_loop()

    def arrow_left(self, function):
        self.screen.onkeypress(function, "Left")

    def arrow_right(self, function):
        self.screen.onkeypress(function, "Right")

    def arrow_up(self, function):
        self.screen.onkeypress(function, "Up")

    def arrow_down(self, function):
        self.screen.onkeypress(function, "Down")

    def key_a(self, function):
        self.screen.onkeypress(function, "a")

    def key_d(self, function):
        self.screen.onkeypress(function, "d")

    def key_w(self, function):
        self.screen.onkeypress(function, "w")

    def key_s(self, function):
        self.screen.onkeypress(function, "s")

    def key_space(self, function):
        self.screen.onkeypress(function, "space")

    @staticmethod
    def is_collision(t1, t2):
        distance_ = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
        if distance_ < 15:
            return True
        else:
            return False

    def game_loop(self):

        self.screen.tracer(0)

        player = Player()
        enemy = Enemy()

        self.screen.listen()
        self.key_a(player.move_left())
        self.key_d(player.move_right())
        self.key_space(player.fire())

        while self.game_on:
            self.screen.update()

            enemy.move()

        self.screen.exitonclick()


game = Game()

# if __name__ == "__main__":
#     win = turtle.Screen()
#     win.tracer(0)
#     player = Player()
#     enemy = Enemy()
#     win.update()
#     win.exitonclick()
#     win.mainloop()
