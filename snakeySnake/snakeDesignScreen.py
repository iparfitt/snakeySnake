import colorsys
import math
import pygame

from snakeySnake.button import Button
from snakeySnake.context import Context
from snakeySnake.screen import Screen


class SnakeDesignScreen(Screen):
    """Handles drawing the screen to design a snake and interactions with the screen"""

    def __init__(self, context: Context) -> None:
        """Initialises a snake design screen
        Args:
            context (Context): A context object containing game data
        """
        super().__init__(context)

        self._default_colour = (211, 211, 211)
        self._snake_design = [self._default_colour]
        self._design_length = len(self._snake_design)
        self._selected_colour = self._default_colour

        # Initialise text
        font = pygame.font.Font("freesansbold.ttf", 32)
        self._text = font.render("Snake Design", True, "grey")
        self._text_rect = self._text.get_rect()
        self._text_rect.center = (
            int(self._context.get_display_size() / 2),
            int(self._context.get_display_size() / 6),
        )
        self._wheel_rect = self._context.get_colour_wheel_image().get_rect()
        self._wheel_rect.center = (
            int(self._context.get_display_size() / 2),
            int(5 * self._context.get_display_size() / 12),
        )

        # Initialise save button
        self._save_button = Button(
            self._context.get_display(),
            int(self._context.get_display_size() / 2),
            int(7 * self._context.get_display_size() / 8),
            "Save",
            20,
            self._save_snake_design,
        )

    def draw(self, events: list) -> None:
        """Displays the snake design screen, ready for keyboard events
        Args:
            events (list): A list of pygame events
        """

        self._context.get_display().fill("black")
        self._context.get_display().blit(self._text, self._text_rect)
        self._context.get_display().blit(
            self._context.get_colour_wheel_image(), self._wheel_rect
        )

        self._design_length = len(self._snake_design)
        for idx in range(self._design_length):
            pygame.draw.rect(
                self._context.get_display(),
                self._snake_design[idx],
                [
                    (
                        self._context.get_display_size() / 2
                        + self._context.get_snake_size()
                        * (2 * idx - self._design_length),
                        3 * self._context.get_display_size() / 4,
                    ),
                    (
                        2 * self._context.get_snake_size(),
                        2 * self._context.get_snake_size(),
                    ),
                ],
                border_radius=int(self._context.get_snake_size() / 4),
            )

        mouse_pos = pygame.mouse.get_pos()
        distance = math.hypot(
            self._wheel_rect.centerx - mouse_pos[0],
            self._wheel_rect.centery - mouse_pos[1],
        )
        if distance <= self._context.get_colour_wheel_radius():
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    angle = math.atan2(
                        mouse_pos[0] - self._wheel_rect.centerx,
                        mouse_pos[1] - self._wheel_rect.centery,
                    )
                    if angle < 0:
                        angle += 2 * math.pi

                    rgb = colorsys.hsv_to_rgb(
                        angle / (2 * math.pi),
                        distance / self._context.get_colour_wheel_radius(),
                        1,
                    )
                    rgb = tuple(int(i * 255) for i in rgb)
                    self._snake_design[-1] = rgb

        if self._design_length < 5:
            plus_button = Button(
                self._context.get_display(),
                int(
                    self._context.get_display_size() / 2
                    + self._context.get_snake_size() * (self._design_length + 1 / 2)
                ),
                int(
                    3 * self._context.get_display_size() / 4
                    + self._context.get_snake_size() / 2
                ),
                "+",
                15,
                self._add_to_snake_design,
            )
            plus_button.process(events)
        if self._design_length > 1:
            minus_button = Button(
                self._context.get_display(),
                int(
                    self._context.get_display_size() / 2
                    + self._context.get_snake_size() * (self._design_length + 1 / 2)
                ),
                int(
                    3 * self._context.get_display_size() / 4
                    + 5 * self._context.get_snake_size() / 4
                ),
                "-",
                15,
                self._remove_from_snake_design,
            )
            minus_button.process(events)

        self._save_button.process(events)

    def _add_to_snake_design(self) -> None:
        """Add an element to the snake design"""
        self._snake_design.append(self._default_colour)

    def _remove_from_snake_design(self) -> None:
        """Remove the back element from the snake design"""
        self._snake_design.pop(-1)

    def _save_snake_design(self) -> None:
        """Saves the snake design"""
        self._context.save_snake_design(self._snake_design)
        self._snake_design = [self._default_colour]
        self._selected_colour = self._default_colour
        self._context.screen_to_start()
