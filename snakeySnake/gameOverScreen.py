import pygame

from snakeySnake.button import Button
from snakeySnake.context import Context
from snakeySnake.screen import Screen


class GameOverScreen(Screen):
    """The screen displayed when the user fails on the game screen"""

    def __init__(self, context: Context) -> None:
        """Initialises a game over screen
        Args:
            context (Context): A context object containing game data
        """
        super().__init__(context)

        # Initialise text
        font = pygame.font.Font("freesansbold.ttf", 32)
        self._text = font.render("Game Over", True, "grey")
        self._text_rect = self._text.get_rect()
        self._text_rect.center = (
            int(self._context.get_display_size() / 2),
            int(self._context.get_display_size() / 3),
        )

        # Initialise buttons
        self._start_button = Button(
            self._context.get_display(),
            int(2 * self._context.get_display_size() / 3),
            int(2 * self._context.get_display_size() / 3),
            "Back to Home",
            20,
            self._context.screen_to_start,
        )
        self._game_button = Button(
            self._context.get_display(),
            int(self._context.get_display_size() / 3),
            int(2 * self._context.get_display_size() / 3),
            "Try Again",
            20,
            self._context.screen_to_game,
        )

    def draw(self, events: list) -> None:
        """Displays the game over screen
        Args:
            events (list): A list of pygame events
        """

        self._context.get_display().blit(self._text, self._text_rect)
        self._context.get_score_board().display_past_scores()
        self._start_button.process(events)
        self._game_button.process(events)
