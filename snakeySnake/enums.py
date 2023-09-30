from enum import Enum

"""An enum describing direction"""
class DirectionEnum(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

"""A enum describing the current screen of the game"""
class ScreenEnum(Enum):
    START = 0
    CONTROLS = 1
    SNAKEDESIGN = 2
    GAME = 3
    SCOREBOARD = 4
    GAMEOVER = 5
    