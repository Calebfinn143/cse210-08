import os
import random

from game.casting.actor import Actor
from game.casting.cast import Cast
from game.casting.rocks import Rocks
from game.casting.gems import Gems

from game.directing.director import Director

from game.services.keyboard_service import KeyboardService
from game.services.video_service import VideoService

from game.shared.color import Color
from game.shared.point import Point


FRAME_RATE = 12
MAX_X = 900
MAX_Y = 600
CELL_SIZE = 20
FONT_SIZE = 20
COLS = 60
ROWS = 40
CAPTION = "Greed"
WHITE = Color(255, 255, 255)
DEFAULT_ARTIFACTS = random.randint(1, 6)


def main():
    
    # create the cast
    cast = Cast()
    
    # create the banner
    banner = Actor()
    banner.set_text("")
    banner.set_position(Point(CELL_SIZE, 0))
    cast.add_actor("banners", banner)
    
    # create the robot
    x = int(460)
    y = int(580)
    position = Point(x, y)

    robot = Actor()
    robot.set_text("#")
    robot.set_position(position)
    cast.add_actor("robots", robot)
    
    # create the artifacts
    for n in range(DEFAULT_ARTIFACTS):
        '''Randomize the gems and rocks'''
        gems_and_rocks = ("*", "O")
        text = random.choice(gems_and_rocks)

        x = random.randint(1, COLS - 1)
        y = 600
        position = Point(x, y)
        position = position.scale(CELL_SIZE)

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = Color(r, g, b)

        if text == "O":
            rocks = Rocks()
            rocks.set_text(text)
            rocks.set_font_size(FONT_SIZE)
            rocks.set_color(color)
            rocks.set_position(position)
            rocks.set_velocity(Point(0, 5))
            cast.add_actor("rocks", rocks)
        else:
            gems = Gems()
            gems.set_text(text)
            gems.set_font_size(FONT_SIZE)
            gems.set_color(color)
            gems.set_position(position)
            gems.set_velocity(Point(0, 5))
            cast.add_actor("gems", gems)
    
    # start the game
    keyboard_service = KeyboardService(CELL_SIZE)
    video_service = VideoService(CAPTION, MAX_X, MAX_Y, CELL_SIZE, FRAME_RATE)
    director = Director(keyboard_service, video_service)
    director.start_game(cast)

if __name__ == "__main__":
    main()