from time import perf_counter as timer

import pygame

from snakeySnake.enums import DirectionEnum

direction_map = {
    DirectionEnum.NONE: (0, 0),
    DirectionEnum.LEFT: (-1, 0),
    DirectionEnum.RIGHT: (1, 0),
    DirectionEnum.UP: (0, -1),
    DirectionEnum.DOWN: (0, 1),
}


class Snake:
    """A class describing the snake and its movements"""

    def __init__(
        self,
        display: pygame.Surface,
        size: int,
        starting_pos: tuple,
        update_interval: float,
        add_time_survived,
        add_apple_collected,
    ) -> None:
        """Initialises a snake object

        Args:
            display             (pygame.Surface): The surface to place the button on
            size                (int): The size of the snake pixels to draw
            starting_pos        (tuple): The starting coord of the snake
            update_interval     (float): The interval to update the snake's movements on
            add_time_survived   (function(float)): A function to call when additional time is survived
            add_apple_collected (function(None)): A function to call when an apple is collected
        """
        self._display = display
        self._size = size

        self._body = [pygame.Rect(starting_pos, (self._size, self._size))]
        self._starting_head = self._body[0]
        self._snake_design = ["#4CFF33"]
        self._num_colours = len(self._snake_design)

        self._body_len = 1
        self._direction_name = DirectionEnum.RIGHT
        self._direction = direction_map[self._direction_name]  # Initially moving right

        self._last_update_time = timer()
        self._update_interval = update_interval
        self._add_time_survived = add_time_survived
        self._add_apple_collected = add_apple_collected

    def get_size(self) -> float:
        """Returns the size of a pixel of the snake"""
        return self._size

    def move(self, direction_name: DirectionEnum) -> None:
        """Move the snake in the specified direction

        Args:
            direction (DirectionEnum): The direction to move the snake in
        """
        self._direction_name = direction_name
        self._direction = direction_map[direction_name]
        self._shift(self._direction[0], self._direction[1])

    def update(self, apple_locations: list) -> None:
        """Update the snake object by moving 1 pixel in the direction of travel

        Args:
            apple_locations (list(tuple)): The locations of apples on the board
        """
        # Move in direction of travel
        if timer() - self._last_update_time > self._update_interval:
            self._add_time_survived(timer() - self._last_update_time)
            self._last_update_time = timer()
            self._check_if_collected_apple(apple_locations)

            # Move snake 1 pixel in the direction of travel
            self._shift(self._direction[0], self._direction[1])

    def start_timer(self) -> None:
        """Update the timer"""
        self._last_update_time = timer()

    def draw(self) -> None:
        """Draw the snake on the screen"""
        for idx in range(self._body_len - 1, -1, -1):
            pygame.draw.rect(
                self._display,
                self._snake_design[idx % self._num_colours],
                self._body[idx],
                border_radius=int(self._size / 4),
            )

    def ran_into_self(self) -> bool:
        """Returns true if the snake has run into itself, false otherwise"""

        for idx in range(2, self._body_len):
            if (
                self.get_head_x() == self._body[idx].x
                and self.get_head_y() == self._body[idx].y
            ):
                return True
        return False

    def save_design(self, snake_design) -> None:
        """Set the snake design"""
        self._snake_design = snake_design
        self._num_colours = len(self._snake_design)

    def reset(self) -> None:
        """Resets the snake to its starting location and size"""

        self._body = [self._starting_head]
        self._body_len = 1
        self._direction_name = DirectionEnum.RIGHT
        self._direction = direction_map[self._direction_name]

    def get_head_x(self) -> float:
        """Returns the current x coordinate of the head"""
        return self._body[0].x

    def get_head_y(self) -> float:
        """Returns the curent y coordinate of the head"""
        return self._body[0].y

    def _shift(self, x_move, y_move) -> None:
        """Shifts every pixel to the location of the pixel ahead"""

        # Every pixel moves to position of pixel ahead, except head
        for idx in range(self._body_len - 1, 0, -1):
            self._body[idx] = self._body[idx - 1]

        # Move head
        self._body[0] = self._body[0].move(
            x_move * 2 * self._size / 3, y_move * 2 * self._size / 3
        )

    def _add_to_tail(self) -> None:
        """Adds a pixel to the tail of the snake"""

        self._body.append(self._body[self._body_len - 1])
        self._body_len += 1
        self._body[self._body_len - 1].move(
            self._direction[0] * -self._size, self._direction[1] * -self._size
        )

    def _check_if_collected_apple(self, apple_locations: list) -> None:
        """Checks if the snake has collected an apple, and adds to the tail if it has

        Args:
            apple_locations (list(tuple)): The locations of all apples on the screen
        """
        for apple in apple_locations:
            if (
                abs(self.get_head_x() - apple[0]) <= 2 * self._size
                and abs(self.get_head_y() - apple[1]) <= 2 * self._size
            ):
                apple_locations.remove(apple)
                self._add_apple_collected()
                self._add_to_tail()
