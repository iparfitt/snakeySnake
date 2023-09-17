from enum import Enum

class Direction(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

class Screen(Enum):
    START = 0
    SCOREBOARD = 1
    TUTORIAL = 2
    GAME = 3