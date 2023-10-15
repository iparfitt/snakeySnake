from abc import ABC, abstractmethod

from snakeySnake.context import Context


class Screen(ABC):
    """An abstract object used to make different screens"""
    def __init__(self, context: Context) -> None:
        """Initialises a base screen object
        Args:
            context (Context): A context object containing game data
        """
        self._context = context

    @abstractmethod
    def draw(self, events: list) -> None:
        """Draws the screen onto a display. Must be overrided.
        Args:
            events (list): A list of pygame events
        """
