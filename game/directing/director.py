from ctypes.wintypes import POINT

from game.casting.rocks import Rocks
from game.casting.gems import Gems
import random
from game.shared.point import Point
from game.shared.color import Color

class Director:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
    """

    def __init__(self, keyboard_service, video_service):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        self._score = 0
        self.DEFAULT_ARTIFACTS = random.randint(0, 6)
        self.FONT_SIZE = 20
        self.CELL_SIZE = 20
        self.COLS = 60
        
    def start_game(self, cast):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.open_window()
        while self._video_service.is_window_open():
            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)
            self._create_artifacts(cast)
        self._video_service.close_window()

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the robot.
        
        Args:
            cast (Cast): The cast of actors.
        """
        robot = cast.get_first_actor("robots")
        velocity = self._keyboard_service.get_direction()
        robot.set_velocity(velocity)        

    def _do_updates(self, cast):
        """Updates the robot's position and resolves any collisions with artifacts.
        
        Args:
            cast (Cast): The cast of actors.
        """
        banner = cast.get_first_actor("banners")
        robot = cast.get_first_actor("robots")
        gems = cast.get_actors("gems")
        rocks = cast.get_actors("rocks")

        banner.set_text("Score: " + str(self._score))
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        robot.move_next(max_x, max_y)

        for gem in gems:
            gem.move_next(max_x, max_y)
            if robot.get_position().equals(gem.get_position()):
                cast.remove_actor("gems", gem)
                self._score += 1
            if gem.get_position().get_y() == 590:
                cast.remove_actor("gems", gem)

        for rock in rocks:
            rock.move_next(max_x, max_y)
            if robot.get_position().equals(rock.get_position()):
                    cast.remove_actor("rocks", rock)
                    self._score -= 1
            if rock.get_position().get_y() == 590:
                cast.remove_actor("rocks", rock)
        
    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()

    def _create_artifacts(self, cast):
        for n in range(self.DEFAULT_ARTIFACTS):
            self.gems_and_rocks = ("*", "O")
            text = random.choice(self.gems_and_rocks)

            x = random.randint(1, self.COLS - 1)
            y = 600
            position = Point(x, y)
            position = position.scale(self.CELL_SIZE)

            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            color = Color(r, g, b)

            if text == "O":
                rocks = Rocks()
                rocks.set_text(text)
                rocks.set_font_size(self.FONT_SIZE)
                rocks.set_color(color)
                rocks.set_position(position)
                rocks.set_velocity(Point(0, 5))
                cast.add_actor("rocks", rocks)
            else:
                gems = Gems()
                gems.set_text(text)
                gems.set_font_size(self.FONT_SIZE)
                gems.set_color(color)
                gems.set_position(position)
                gems.set_velocity(Point(0, 5))
                cast.add_actor("gems", gems)