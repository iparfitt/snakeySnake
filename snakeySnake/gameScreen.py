import pygame
import random
import time

from snakeySnake.context import Context
from snakeySnake.enums import DirectionEnum, ScreenEnum
from snakeySnake.screen import Screen

class GameScreen(Screen):
    def __init__(self, context: Context) -> None:
        """Initialise a game screen
        Args:
            context (Context): A context object containing game data
        """
        super().__init__(context)

        self._lastUpdateTime = time.perf_counter()
        self._lastAppleTime = time.perf_counter()

        self._appleLocations = []

    def draw(self, events: list) -> None:
        """Displays the game screen, ready for keyboard events
        Args:
            events (list): A list of pygame events
        """

        while (self._context.getCurrentScreen() == ScreenEnum.GAME):
            for event in pygame.event.get():
                # Move snake based on key movements
                if (event.type == pygame.KEYDOWN):
                    direction = DirectionEnum.NONE
                    if ((event.key == pygame.K_w) or
                        (event.key == pygame.K_UP)):
                        direction = DirectionEnum.UP
                    elif ((event.key == pygame.K_s) or
                        (event.key == pygame.K_DOWN)):
                        direction = DirectionEnum.DOWN
                    elif ((event.key == pygame.K_a) or
                        (event.key == pygame.K_LEFT)):
                        direction = DirectionEnum.LEFT
                    elif ((event.key == pygame.K_d) or
                        (event.key == pygame.K_RIGHT)):
                        direction = DirectionEnum.RIGHT
                    self._context.getSnake().move(direction)
            self._context.getSnake().update(self._appleLocations)
            
            self._context.getDisplay().fill("grey")
            pygame.draw.rect(self._context.getDisplay(), 
                             "black", 
                             [self._context.getBorderWidth(), 
                              self._context.getBorderWidth(), 
                              self._context.getGameSize() - self._context.getBorderWidth(), 
                              self._context.getGameSize() - self._context.getBorderWidth()])

            self._drawApples()
            self._context.getSnake().draw()
            self._context.getScoreBoard().displayCurrentScore(self._context.getBorderWidth())
            self._checkGameOver()
            pygame.display.flip()
            self._context.updateTimer()

    def _drawApples(self) -> None:
        """Draw apples in a random location if time since the last apple has elapsed"""

        if time.perf_counter() - self._lastAppleTime > 5.0:
            self._lastAppleTime = time.perf_counter()
            self._appleLocations.extend([(random.randint(self._context.getBorderWidth(), self._context.getGameSize() - self._context.getAppleSize()),
                                          random.randint(self._context.getBorderWidth(), self._context.getGameSize() - self._context.getAppleSize()))])

        for apple in self._appleLocations:
            self._context.getDisplay().blit(self._context.getAppleImage(), apple)

    def _checkGameOver(self) -> None:
        """Runs cleanup if the game is over, including writing the current score to file and resetting the game"""

        x = self._context.getSnake().getHeadX()
        y = self._context.getSnake().getHeadY()

        if (x >= self._context.getGameSize() or
            x <= self._context.getBorderWidth() or
            y >= self._context.getGameSize() or
            y <= self._context.getBorderWidth() or
            self._context.getSnake().ranIntoItself()):

            self._context.screenToGameOver()
            self._context.getScoreBoard().writeToFile()
            self._context.getSnake().reset()
            self._appleLocations.clear()
