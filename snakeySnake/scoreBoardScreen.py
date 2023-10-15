import pygame

from snakeySnake.button import Button
from snakeySnake.context import Context
from snakeySnake.screen import Screen


class ScoreBoardScreen(Screen):
    """The screen to display past scores"""

    def __init__(self, context: Context):
        """Initialises a score board screen
        Args:
            context (Context): A context object containing game data
        """
        super().__init__(context)

        # Initialise text
        font = pygame.font.Font("freesansbold.ttf", 32)
        self._text = font.render("Score Board", True, "grey")
        self._text_rect = self._text.get_rect()
        self._text_rect.center = (
            int(self._context.get_display_size() / 2),
            int(self._context.get_display_size() / 3),
        )

        # Initialise button
        self._start_button = Button(
            self._context.get_display(),
            int(self._context.get_display_size() / 2),
            int(2 * self._context.get_display_size() / 3),
            "Back to Home",
            20,
            self._context.screen_to_start,
        )

    def draw(self, events: list) -> None:
        """Displays the current local scoreboard
        Args:
            events (list) A list of pygame events
        """

        self._context.get_display().fill("black")
        self._context.get_display().blit(self._text, self._text_rect)
        self._context.get_score_board().display_past_scores()
        self._start_button.process(events)
