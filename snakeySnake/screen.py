from abc import ABC, abstractmethod

from snakeySnake.context import Context

class Screen(ABC):
    def __init__(self, context: Context):
        self._context = context

    @abstractmethod
    def draw(self):
        pass