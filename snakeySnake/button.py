import pygame


class Button:
    """A Class that defines a button that can be pressed in a display"""

    def __init__(
        self,
        display: pygame.Surface,
        x: int,
        y: int,
        text: str,
        font_size: int,
        on_click,
    ) -> None:
        """Initialises a button object

        Args:
            display   (pygame.Surface): The surface to place the button on
            x         (int): The left x value of the button
            y         (int): The top y value of the button
            text      (str): The text to display on the button
            font_size (int): The font size of the text
            on_click  (function(None)): The function to play when the button is clicked
        """
        self._display = display

        font = pygame.font.Font("freesansbold.ttf", font_size)
        self._text = font.render(text, True, "black")
        self._text_rect = self._text.get_rect()
        self._text_rect.center = (x, y)
        self._button_surface = pygame.Surface((len(text) * 0.75 * font_size, font_size))
        self._button_rect = pygame.Rect(0, 0, len(text) * 0.75 * font_size, font_size)
        self._button_rect.center = (x, y)

        self._on_click = on_click

        self._fill_colours = {
            "normal": "#ffffff",
            "hover": "#666666",
            "pressed": "#333333",
        }

    def process(self, events: list) -> None:
        """Determine if the button has been pressed, and change the surface accordingly
        Args:
            events (list): A list of pygame events
        """

        if self._is_pressed(events):
            self._on_click()

        self._button_surface.blit(
            self._text,
            [
                self._button_rect.width / 2 - self._text_rect.width / 2,
                self._button_rect.height / 2 - self._text_rect.height / 2,
            ],
        )
        self._display.blit(self._button_surface, self._button_rect)

    def _is_pressed(self, events: list) -> bool:
        """Return true if the button has been pressed, false otherwise
        Args:
            events (list): A list of pygame events
        """

        self._button_surface.fill(self._fill_colours["normal"])
        if self._button_rect.collidepoint(pygame.mouse.get_pos()):
            self._button_surface.fill(self._fill_colours["hover"])

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._button_surface.fill(self._fill_colours["pressed"])
                    return True
        return False
