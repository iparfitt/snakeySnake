import pygame

from snakeySnake.button import Button
from snakeySnake.context import Context
from snakeySnake.screen import Screen


class ControlScreen(Screen):
    """A screen to describe the controls to play the game"""

    def __init__(self, context: Context) -> None:
        """Initialises a controls screen
        Args:
            context (Context): A context object containing game data
        """
        super().__init__(context)
        self._display = self._context.get_display()

        # Initialise text
        font = pygame.font.Font("freesansbold.ttf", 32)
        self._title = font.render("Controls", True, "grey")
        self._title_rect = self._title.get_rect()
        self._title_rect.center = (
            int(self._context.get_display_size() / 2),
            int(self._context.get_display_size() / 3),
        )
        self._text_buffer = 40

        font = pygame.font.Font("freesansbold.ttf", 20)
        self._text_strings = [
            "- Move your snake using 'ASWD' or the arrow keys",
            "- Collect",
            "- Don't run into yourself or the walls",
            "Good Luck!",
        ]
        self._text_rects = []
        self._text_surfaces = []
        buffer = self._text_buffer
        for line in self._text_strings:
            text = font.render(line, True, "white")
            text_rect = text.get_rect()
            text_rect.center = (
                int(self._context.get_display_size() / 2),
                int(self._context.get_display_size() / 3 + buffer),
            )
            self._text_surfaces.append(text)
            self._text_rects.append(text_rect)
            buffer += self._text_buffer

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
        """Displays the controls for the snake game
        Args:
            events (list): A list of pygame events
        """

        self._display.fill("black")
        self._display.blit(self._title, self._title_rect)

        for idx, line in enumerate(self._text_strings):
            self._display.blit(self._text_surfaces[idx], self._text_rects[idx])

            if line == "- Collect":
                self._display.blit(
                    self._context.get_apple_image(),
                    (self._text_rects[idx].right + 2, self._text_rects[idx].top - 8),
                )

        self._start_button.process(events)
