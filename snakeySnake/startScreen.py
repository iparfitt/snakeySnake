import pygame

from snakeySnake.button import Button
from snakeySnake.context import Context
from snakeySnake.screen import Screen


class StartScreen(Screen):
    """Initial game screen"""

    def __init__(self, context: Context) -> None:
        """Initialises a start screen
        Args:
            context (Context) A context object containing game data
        """
        super().__init__(context)

        # Initialise text
        font = pygame.font.Font("freesansbold.ttf", 60)
        self._text = font.render("SnakeySnake", True, "white")
        self._text_rect = self._text.get_rect()
        self._text_rect.center = (
            int(self._context.get_display_size() / 2),
            int(self._context.get_display_size() / 2),
        )

        # Initialise buttons
        self._controls_button = Button(
            self._context.get_display(),
            int(5 * self._context.get_display_size() / 6),
            int(self._context.get_display_size() / 14),
            "Controls",
            20,
            self._context.screen_to_controls,
        )
        self._snake_design_button = Button(
            self._context.get_display(),
            int(self._context.get_display_size() / 6),
            int(2 * self._context.get_display_size() / 3),
            "Snake Design",
            20,
            self._context.screen_to_snake_design,
        )
        self._start_button = Button(
            self._context.get_display(),
            int(self._context.get_display_size() / 2),
            int(2 * self._context.get_display_size() / 3),
            "Start Game",
            20,
            self._context.screen_to_game,
        )
        self._score_board_button = Button(
            self._context.get_display(),
            int(5 * self._context.get_display_size() / 6),
            int(2 * self._context.get_display_size() / 3),
            "Score Board",
            20,
            self._context.screen_to_score_board,
        )

    def draw(self, events: list) -> None:
        """Displays the start screen, ready for keyboard events
        Args:
            events (list): A list of pygame events
        """

        self._context.get_display().fill("black")
        for i in range(
            0,
            self._context.get_display_size(),
            int(self._context.get_apple_size() * 4.6),
        ):
            for j in range(
                0,
                self._context.get_display_size(),
                int(self._context.get_apple_size() * 4.6),
            ):
                self._context.get_display().blit(
                    self._context.get_apple_image(), (i, j)
                )

        self._context.get_display().blit(self._text, self._text_rect)
        self._controls_button.process(events)
        self._snake_design_button.process(events)
        self._start_button.process(events)
        self._score_board_button.process(events)
