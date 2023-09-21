from enum import Enum

"""An enum describing direction"""
class Direction(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

"""A enum describing the current screen of the game"""
class Screen(Enum):
    START = 0
    SCOREBOARD = 1
    TUTORIAL = 2
    GAME = 3
    GAMEOVER = 4