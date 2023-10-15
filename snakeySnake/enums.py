from enum import Enum


class DirectionEnum(Enum):
    """An enum describing direction"""

    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class ScreenEnum(Enum):
    """A enum describing the current screen of the game"""

    START = 0
    CONTROLS = 1
    SNAKEDESIGN = 2
    GAME = 3
    SCOREBOARD = 4
    GAMEOVER = 5
