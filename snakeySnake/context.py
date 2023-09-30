from pathlib import Path
import pygame

from snakeySnake.enums import ScreenEnum
from snakeySnake.scoreboard import ScoreBoard
from snakeySnake.snake import Snake

class Context:
    def __init__(self):
        self._displaySize = 600
        self._borderWidth = 10
        self._gameSize = self._displaySize - self._borderWidth
        self._fps = 60
        self._fpsClock = pygame.time.Clock()

        # Initialise board
        pygame.init()
        self._display = pygame.display.set_mode((self._displaySize, self._displaySize))
        self._screen = ScreenEnum.START
        pygame.display.update()
        pygame.display.set_caption('Snake Game')

        self._snakeSize = 20
        self._appleSize = self._snakeSize * 2
        self._colourWheelRadius = self._snakeSize * 5

        self._scoreBoard = ScoreBoard(self._display)
        self._snake = Snake(self._display,
                            self._snakeSize,
                            (self._displaySize/2,
                             self._displaySize/2),
                            0.05, 
                            self._scoreBoard.addTimeSurvived, 
                            self._scoreBoard.addAppleCollected)

        self._appleImage = pygame.image.load(str(Path(__file__).parent.absolute()) + "/data/apple.png").convert()
        self._appleImage = pygame.transform.scale(self._appleImage, (self._appleSize, self._appleSize))
        
        self._colourWheelRadius = self._snake.getSize() * 5
        self._colourWheelImage = pygame.image.load(str(Path(__file__).parent.absolute()) + "/data/colour_wheel.png").convert()
        self._colourWheelImage = pygame.transform.scale(self._colourWheelImage, (self._colourWheelRadius*2, self._colourWheelRadius*2))

    def getDisplaySize(self):
        return self._displaySize

    def getBorderWidth(self):
        return self._borderWidth
    
    def getGameSize(self):
        return self._displaySize - self._borderWidth
    
    def getSnakeSize(self):
        return self._snakeSize
    
    def getAppleSize(self):
        return self._appleSize
    
    def getColourWheelRadius(self):
        return self._colourWheelRadius
    
    def getCurrentScreen(self):
        return self._screen
    
    def getDisplay(self):
        return self._display
    
    def getAppleImage(self):
        return self._appleImage
    
    def getColourWheelImage(self):
        return self._colourWheelImage
    
    def getScoreBoard(self):
        return self._scoreBoard
    
    def getSnake(self):
        return self._snake
    
    def saveSnakeDesign(self, snakeDesign):
        self._snake.saveDesign(snakeDesign)

    def updateTimer(self):
        self._fpsClock.tick(self._fps)

    def screenToStart(self) -> None:
        """Changes the screen to the start screen"""
        self._screen = ScreenEnum.START
    
    def screenToControls(self) -> None:
        """Changes the screen to the controls screen"""
        self._screen = ScreenEnum.CONTROLS

    def screenToSnakeDesign(self) -> None:
        """Changes the screen to the snake design screen"""
        self._screen = ScreenEnum.SNAKEDESIGN
        self._snakeDesign = ['#ffffff']
        self._selectedColour = (255, 100, 0)
    
    def screenToGame(self) -> None:
        """Changes the screen to the game screen"""
        self._screen = ScreenEnum.GAME
        self._snake.startTimer()
        self._scoreBoard.reset()

    def screenToScoreBoard(self) -> None:
        """Changes the screen to the scoreboard screen"""
        self._screen = ScreenEnum.SCOREBOARD
    
    def screenToGameOver(self) -> None:
        """Changes the screen to the game over screen"""
        self._screen = ScreenEnum.GAMEOVER