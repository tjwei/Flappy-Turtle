#!/usr/bin/env python3
# Author: tjw (https://github.com/tjwei/Flappy-Turtle)
# Welcome to PyCon APAC 2014/Taiwan!
# More info on https://tw.pycon.org/2014apac/

from turtle import *
from time import time, sleep
from random import randint
from subprocess import Popen
import sys
import glob


def play_sound(name, vol=100):
    file_name = name + ".mp3"
    if sys.platform == "darwin":
        cmds = ["afplay"]
    else:
        cmds = ["mplayer", "-softvol", "-really-quiet", "-volume", str(vol)]
    try:
        Popen(cmds + [file_name])
    except:
        pass

screensize(216, 500)
setup(288, 512)
tracer(False, 0)
hideturtle()
for f in glob.glob("*.gif"):
    addshape(f)

font_name = "Comic Sans MS"
speed_x = 100
ground_line = -200 + 56 + 12
tube_dist = 230
bg_width = 286


def TextTurtle(x, y, color):
    t = Turtle()
    t.hideturtle()
    t.up()
    t.goto(x, y)
    t.speed(0)
    t.color(color)
    return t


def GIFTurtle(fname):
    t = Turtle(fname + ".gif")
    t.speed(0)
    t.up()
    return t

score_txt = TextTurtle(0, 130, "white")
best_txt = TextTurtle(90, 180, "white")
pycon_apac_txt = TextTurtle(0, -270, "white")
bgpic("bg1.gif")
tubes = [(GIFTurtle("tube1"), GIFTurtle("tube2")) for i in range(3)]
grounds = [GIFTurtle("ground") for i in range(3)]
bird = GIFTurtle("bird1")

PYCON_APAC_AD = """\
     More Fun at
PyCon APAC 2014/TW
"""

class Game:
    state = "end"
    score = best = 0
game = Game()


def start_game(game):
    game.best = max(game.score, game.best)
    game.tubes_y = [10000] * 3
    game.hit_t, game.hit_y = 0, 0
    game.state = "alive"
    game.tube_base = 0
    game.score = 0
    game.start_time = time()
    pycon_apac_txt.clear()
    update_game(game)


def compute_y(t, game):
    return game.hit_y - 100 * (t - game.hit_t) * (t - game.hit_t - 1)


def update_game(game):
    if game.state == "dead":
        play_sound("clickclick")
        pycon_apac_txt.write(
            PYCON_APAC_AD,
            align="center",
            font=(font_name, 24, "bold")
        )
        sleep(2)
        game.state = "end"
        return
    t = time() - game.start_time
    bird_y = compute_y(t, game)
    if bird_y <= ground_line:
        bird_y = ground_line
        game.state = "dead"
    x = int(t * speed_x)
    tube_base = -(x % tube_dist) - 40
    if game.tube_base < tube_base:
        if game.tubes_y[2] < 1000:
            game.score += 1
            play_sound("bip")
        game.tubes_y = game.tubes_y[1:] + [randint(-100, 50)]
    game.tube_base = tube_base
    for i in range(3):
        tubes[i][0].goto(
            tube_base + tube_dist * (i - 1), 250 + game.tubes_y[i])
        tubes[i][1].goto(
            tube_base + tube_dist * (i - 1), -150 + game.tubes_y[i])
    if game.tubes_y[2] < 1000:
        tube_left = tube_base + tube_dist - 28
        tube_right = tube_base + tube_dist + 28
        tube_upper = game.tubes_y[2] + 250 - 160
        tube_lower = game.tubes_y[2] - 150 + 160
        center = Vec2D(0, bird_y - 2)
        lvec = Vec2D(tube_left, tube_upper) - center
        rvec = Vec2D(tube_right, tube_upper) - center
        if (tube_left < 18 and tube_right > -18) and bird_y - 12 <= tube_lower:
            game.state = "dead"
        if (tube_left <= 8 and tube_right >= -8) and bird_y + 12 >= tube_upper:
            game.state = "dead"
        if abs(lvec) < 14 or abs(rvec) < 14:
            game.state = "dead"
    bg_base = -(x % bg_width)
    for i in range(3):
        grounds[i].goto(bg_base + bg_width * (i - 1), -200)
    bird.shape("bird%d.gif" % abs(int(t * 4) % 4 - 1))
    bird.goto(0, bird_y)
    score_txt.clear()
    score_txt.write(
        "%s" % (game.score), align="center", font=(font_name, 80, "bold"))
    if game.best:
        best_txt.clear()
        best_txt.write(
            "BEST: %d" % (game.best), align="center", font=(font_name, 14, "bold"))
    update()
    ontimer(lambda: update_game(game), 10)


def fly(game=game):
    if game.state == "end":
        start_game(game)
        return
    t = time() - game.start_time
    bird_y = compute_y(t, game)
    if bird_y > ground_line:
        game.hit_t, game.hit_y = t, bird_y
        play_sound("tack", 20)

onkey(fly, "space")
listen()
mainloop()
sys.exit(1)
