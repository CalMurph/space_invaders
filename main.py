import tkinter
import turtle
from turtle import Turtle, Screen
import time
import math
import random


class SpaceRaiders:

    def __init__(self):
        self.game_over_text = None
        self.hearts = []
        self.level_text = None
        self.level = 1
        self.missiles = []
        self.scoreboard = None
        self.lives_text = None
        self.move_distance = 10
        self.game_on = True
        self.lives = 3
        self.font = ("Courier", 24)
        self.aliens = []
        self.bullets = []
        self.turrets = []
        self.barriers = []
        self.screen = Screen()
        self.screen.tracer(0)
        self.screen.setup(width=700, height=600)
        self.screen.bgcolor("black")
        self.interval = 500

        self.score = 0

        try:
            self.screen.register_shape("alien.gif")
        except tkinter.TclError:
            print("Cannot read file.")

        try:
            self.screen.register_shape("heart.gif")
        except tkinter.TclError:
            print("Cannot read file.")

        self.create_turret()
        self.create_barriers()
        self.create_aliens()
        self.update_lives()
        self.update_scoreboard()
        self.update_level()
        self.screen.update()

        self.last_fire_time = 0  # Variable to store the last fire time
        self.fire_cooldown = 0.5  # Cooldown period in seconds

        self.screen.listen()
        self.screen.onkey(self.move_left, "Left")
        self.screen.onkey(self.move_right, "Right")
        self.screen.onkey(self.fire_shot, "space")

        time.sleep(1)

        self.move_aliens()

        self.screen.ontimer(self.fire_missile, 1500)

        self.move_bullets()
        self.move_missiles()
        self.detect_collisions_with_aliens()
        self.screen.exitonclick()

    def create_turret(self):
        for i in range(1, 4):
            turret = Turtle("square")
            turret.penup()
            turret.color("darkgreen")
            turret.shapesize(stretch_len=4 / i)
            self.turrets.append(turret)

        self.turrets[0].goto(0, -258)
        self.turrets[1].goto(0, -248)
        self.turrets[2].goto(0, -240)

    def create_barriers(self):
        x = -280
        y = -150

        for i in range(3):
            for _ in range(7):
                barrier = Turtle()
                barrier.penup()
                barrier.color("white")
                barrier.shape("square")
                barrier.goto(x, y)
                self.barriers.append(barrier)
                x += 20
            x += 80

    def move_left(self):
        if self.game_on:
            for turret in self.turrets:
                turret.goto(turret.xcor() - 10, turret.ycor())
            self.screen.update()

    def move_right(self):
        if self.game_on:
            for turret in self.turrets:
                turret.goto(turret.xcor() + 10, turret.ycor())
            self.screen.update()

    def fire_shot(self):
        if self.game_on:
            current_time = time.time()
            if current_time - self.last_fire_time >= self.fire_cooldown:
                bullet = Turtle("square")
                bullet.color("red")
                bullet.shapesize(stretch_wid=0.75, stretch_len=0.125)
                bullet.penup()
                # Position the bullet at the topmost part of the turret
                bullet.goto(self.turrets[2].xcor(), self.turrets[2].ycor() + 10)
                self.bullets.append(bullet)
                self.last_fire_time = current_time

    def fire_missile(self):
        if self.game_on:
            missile = Turtle("square")
            missile.color("blue")
            missile.shapesize(stretch_wid=0.75, stretch_len=0.125)
            missile.penup()

            try:

                random_alien = random.choice(self.aliens)
                missile.goto(random_alien.xcor(), random_alien.ycor())
            except IndexError:
                print("Look over")
                print(self.aliens)

            # missile.goto(random_alien.xcor(), random_alien.ycor())
            self.missiles.append(missile)

            self.screen.ontimer(self.fire_missile, 1500)

    def move_missiles(self):
        if self.game_on:
            for missile in self.missiles[:]:
                y = missile.ycor()
                if y < 300:
                    missile.goto(missile.xcor(), missile.ycor() - 10)
                else:
                    missile.hideturtle()
                    self.missiles.remove(missile)
            self.screen.update()
            self.detect_collision_with_missiles()
            self.detect_collision_with_turret()
            self.screen.ontimer(self.move_missiles, 50)

    def detect_collision_with_missiles(self):
        for missile in self.missiles[:]:
            for barrier in self.barriers[:]:
                if barrier.distance(missile) < 20:
                    barrier.hideturtle()
                    self.barriers.remove(barrier)
                    barrier.goto(-3500, 2000)
                    missile.hideturtle()
                    missile.goto(-3000, -2000)

    def detect_collision_with_turret(self):
        for missile in self.missiles[:]:
            for turret in self.turrets[:]:
                if turret.distance(missile) < 30:
                    for turret1 in self.turrets:
                        turret1.hideturtle()
                    for missile1 in self.missiles:
                        missile1.hideturtle()
                    time.sleep(1)
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_over()
                    self.update_lives()
                    self.missiles.clear()
                    self.turrets.clear()
                    self.create_turret()
                    self.screen.update()
                    break

    def move_bullets(self):
        for bullet in self.bullets[:]:
            y = bullet.ycor()
            if y < 300:
                bullet.goto(bullet.xcor(), bullet.ycor() + 10)
            else:
                bullet.hideturtle()
                self.bullets.remove(bullet)
        self.screen.update()
        self.screen.ontimer(self.move_bullets, 50)

        self.detect_collisions_with_aliens()
        self.detect_collision_with_barriers()

    def create_aliens(self):
        x_start = -200
        y_start = 200
        x_offset = 50
        y_offset = 50
        rows = 3
        cols = 11

        for row in range(rows):
            for col in range(cols):
                alien = Turtle()
                try:
                    alien.shape("alien.gif")
                except turtle.TurtleGraphicsError:
                    alien.shape("turtle")
                    alien.color("green")
                    alien.shapesize(1.5)
                alien.penup()
                alien.goto(x_start + col * x_offset, y_start - row * y_offset)
                self.aliens.append(alien)

    def detect_collisions_with_aliens(self):
        for bullet in self.bullets[:]:
            for alien in self.aliens[:]:
                if alien.distance(bullet) < 30 and bullet.xcor() < 300:
                    alien.hideturtle()
                    alien.goto(-3500, 2000)
                    self.aliens.remove(alien)
                    # bullet.hideturtle()
                    bullet.goto(-3000, -2000)
                    self.score += 10
                    self.update_scoreboard()

        if len(self.aliens) == 0:
            self.screen.update()
            for bullet in self.bullets:
                bullet.hideturtle()
                bullet.goto(-3000, -2000)
            self.screen.update()

            self.level_up()

    def detect_collision_with_barriers(self):
        for bullet in self.bullets[:]:
            for barrier in self.barriers[:]:
                if barrier.distance(bullet) < 20 and bullet.xcor() < 300:
                    barrier.hideturtle()
                    self.barriers.remove(barrier)
                    barrier.goto(-3500, 2000)
                    # bullet.hideturtle()
                    bullet.goto(-3000, -2000)

    def move_aliens(self):
        for alien in self.aliens:
            alien.forward(self.move_distance)

        # Check for boundary collisions and change direction
        if any(alien.xcor() > 300 for alien in self.aliens) or any(alien.xcor() < -300 for alien in self.aliens):
            self.move_distance *= -1
            for alien in self.aliens:
                alien.goto(alien.xcor(), alien.ycor() - 10)

        self.detect_collision_with_ship()

        self.screen.update()

        if self.game_on:
            self.screen.ontimer(self.move_aliens, self.interval)

    def detect_collision_with_ship(self):

        for alien in self.aliens:
            for turret in self.turrets:
                if alien.distance(turret) < 25:
                    self.game_over()
                if alien.ycor() < -280:
                    self.game_over()

    def update_lives(self):

        x = -230
        y = 273

        for heart in self.hearts:
            heart.hideturtle()

        if self.lives_text:
            self.lives_text.clear()

        self.lives_text = Turtle()
        self.lives_text.penup()
        self.lives_text.hideturtle()
        self.lives_text.color("white")
        self.lives_text.goto(-330, 260)
        self.lives_text.write("LIVES: ", align="left", font=self.font)

        self.hearts.clear()

        for i in range(self.lives):
            heart = Turtle()
            try:
                heart.shape("heart.gif")
            except turtle.TurtleGraphicsError:
                heart.shape("circle")
                heart.color("red")
                heart.shapesize(1)
            heart.penup()
            # heart.color("white")
            heart.goto(x, y)
            self.hearts.append(heart)

            x += 30

    def update_scoreboard(self):

        if self.scoreboard:
            self.scoreboard.clear()

        self.scoreboard = Turtle()
        self.scoreboard.penup()
        self.scoreboard.hideturtle()
        self.scoreboard.goto(150, 260)
        self.scoreboard.color("white")
        self.scoreboard.write(f"SCORE: {self.score}", font=self.font)

    def level_up(self):

        self.interval = math.floor(self.interval / 1.5)
        self.level += 1
        self.update_level()

        time.sleep(2)

        self.create_aliens()

    def update_level(self):

        if self.level_text:
            self.level_text.clear()

        self.level_text = Turtle()
        self.level_text.color("white")
        self.level_text.penup()
        self.level_text.hideturtle()
        self.level_text.goto(0, 260)
        self.level_text.write(f"LEVEL {self.level}", align="center", font=self.font)
        
    def game_over(self):
        self.game_over_text = Turtle()
        self.game_over_text.hideturtle()
        self.game_over_text.color("red")
        self.game_over_text.goto(0, 0)
        self.game_over_text.write("GAME OVER!", font=("Courier", 50), align="Center")
        self.game_on = False
        

if __name__ == '__main__':
    game = SpaceRaiders()
