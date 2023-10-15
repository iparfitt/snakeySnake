import random
import time

import pygame

from snakeySnake.context import Context
from snakeySnake.enums import DirectionEnum, ScreenEnum
from snakeySnake.screen import Screen


class GameScreen(Screen):
    """Draws the main game screen and handles key interactions"""

    def __init__(self, context: Context) -> None:
        """Initialise a game screen
        Args:
            context (Context): A context object containing game data
        """
        super().__init__(context)

        self._last_update_time = time.perf_counter()
        self._last_apple_time = time.perf_counter()

        self._apple_locations = []

    def draw(self, events: list) -> None:
        """Displays the game screen, ready for keyboard events
        Args:
            events (list): A list of pygame events
        """

        while self._context.get_current_screen() == ScreenEnum.GAME:
            for event in pygame.event.get():
                # Move snake based on key movements
                if event.type == pygame.KEYDOWN:
                    direction = DirectionEnum.NONE
                    if (event.key == pygame.K_w) or (event.key == pygame.K_UP):
                        direction = DirectionEnum.UP
                    elif (event.key == pygame.K_s) or (event.key == pygame.K_DOWN):
                        direction = DirectionEnum.DOWN
                    elif (event.key == pygame.K_a) or (event.key == pygame.K_LEFT):
                        direction = DirectionEnum.LEFT
                    elif (event.key == pygame.K_d) or (event.key == pygame.K_RIGHT):
                        direction = DirectionEnum.RIGHT
                    self._context.get_snake().move(direction)
            self._context.get_snake().update(self._apple_locations)

            self._context.get_display().fill("grey")
            pygame.draw.rect(
                self._context.get_display(),
                "black",
                [
                    self._context.get_border_width(),
                    self._context.get_border_width(),
                    self._context.get_game_size() - self._context.get_border_width(),
                    self._context.get_game_size() - self._context.get_border_width(),
                ],
            )

            self._draw_apples()
            self._context.get_snake().draw()
            self._context.get_score_board().display_current_score(
                self._context.get_border_width()
            )
            self._check_game_over()
            pygame.display.flip()
            self._context.update_timer()

    def _draw_apples(self) -> None:
        """Draw apples in a random location if time since the last apple has elapsed"""

        if time.perf_counter() - self._last_apple_time > 5.0:
            self._last_apple_time = time.perf_counter()
            self._apple_locations.extend(
                [
                    (
                        random.randint(
                            self._context.get_border_width(),
                            self._context.get_game_size()
                            - self._context.get_apple_size(),
                        ),
                        random.randint(
                            self._context.get_border_width(),
                            self._context.get_game_size()
                            - self._context.get_apple_size(),
                        ),
                    )
                ]
            )

        for apple in self._apple_locations:
            self._context.get_display().blit(self._context.get_apple_image(), apple)

    def _check_game_over(self) -> None:
        """Runs cleanup if the game is over, including writing the current score to file and resetting the game"""

        x = self._context.get_snake().get_head_x()
        y = self._context.get_snake().get_head_y()

        if (
            x >= self._context.get_game_size()
            or x <= self._context.get_border_width()
            or y >= self._context.get_game_size()
            or y <= self._context.get_border_width()
            or self._context.get_snake().ran_into_self()
        ):
            self._context.screen_to_game_over()
            self._context.get_score_board().write_to_file()
            self._context.get_snake().reset()
            self._apple_locations.clear()
