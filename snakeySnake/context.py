from pathlib import Path
import pygame

from snakeySnake.enums import ScreenEnum
from snakeySnake.scoreboard import ScoreBoard
from snakeySnake.snake import Snake


class Context:
    """Contains common data shared across screens"""

    def __init__(self) -> None:
        """Initialises a context object"""

        self._display_size = 600
        self._border_width = 10
        self._game_size = self._display_size - self._border_width
        self._fps = 60
        self._fps_clock = pygame.time.Clock()

        # Initialise board
        pygame.init()
        self._display = pygame.display.set_mode(
            (self._display_size, self._display_size)
        )
        self._screen = ScreenEnum.START
        pygame.display.update()
        pygame.display.set_caption("Snake Game")

        self._snake_size = 20
        self._apple_size = self._snake_size * 2
        self._colour_wheel_radius = self._snake_size * 5

        # Initialises other objects
        self._score_board = ScoreBoard(self._display)
        self._snake = Snake(
            self._display,
            self._snake_size,
            (self._display_size / 2, self._display_size / 2),
            0.05,
            self._score_board.add_time_survived,
            self._score_board.add_apple_collected,
        )

        # Resize images
        self._apple_image = pygame.image.load(
            str(Path(__file__).parent.absolute()) + "/data/apple.png"
        ).convert()
        self._apple_image = pygame.transform.scale(
            self._apple_image, (self._apple_size, self._apple_size)
        )

        self._colour_wheel_radius = self._snake.get_size() * 5
        self._colour_wheel_image = pygame.image.load(
            str(Path(__file__).parent.absolute()) + "/data/colour_wheel.png"
        ).convert()
        self._colour_wheel_image = pygame.transform.scale(
            self._colour_wheel_image,
            (self._colour_wheel_radius * 2, self._colour_wheel_radius * 2),
        )

    def get_display_size(self):
        """Returns the size of the display"""
        return self._display_size

    def get_border_width(self):
        """Returns the width of the border on the display"""
        return self._border_width

    def get_game_size(self):
        """Returns the size of the portion of display the game is played in"""
        return self._display_size - self._border_width

    def get_snake_size(self):
        """Returns the size of a pixel of the snake"""
        return self._snake_size

    def get_apple_size(self):
        """Returns the size of the apple image"""
        return self._apple_size

    def get_colour_wheel_radius(self) -> float:
        """Returns the radius of the colour wheel"""
        return self._colour_wheel_radius

    def get_current_screen(self):
        """Returns the enum describing the current screen"""
        return self._screen

    def get_display(self):
        """Returns the display object screens are drawn on"""
        return self._display

    def get_apple_image(self):
        """Returns the apple image"""
        return self._apple_image

    def get_colour_wheel_image(self):
        """Returns the colour wheel image"""
        return self._colour_wheel_image

    def get_score_board(self):
        """Returns the score board object scores are recorded to"""
        return self._score_board

    def get_snake(self):
        """Returns the snake object"""
        return self._snake

    def save_snake_design(self, snake_design):
        """Saves the snake design to the snake"""
        self._snake.save_design(snake_design)

    def update_timer(self):
        """Updates the current timer"""
        self._fps_clock.tick(self._fps)

    def screen_to_start(self) -> None:
        """Changes the screen to the start screen"""
        self._screen = ScreenEnum.START

    def screen_to_controls(self) -> None:
        """Changes the screen to the controls screen"""
        self._screen = ScreenEnum.CONTROLS

    def screen_to_snake_design(self) -> None:
        """Changes the screen to the snake design screen"""
        self._screen = ScreenEnum.SNAKEDESIGN

    def screen_to_game(self) -> None:
        """Changes the screen to the game screen"""
        self._screen = ScreenEnum.GAME
        self._snake.start_timer()
        self._score_board.reset()

    def screen_to_score_board(self) -> None:
        """Changes the screen to the scoreboard screen"""
        self._screen = ScreenEnum.SCOREBOARD

    def screen_to_game_over(self) -> None:
        """Changes the screen to the game over screen"""
        self._screen = ScreenEnum.GAMEOVER
