import pygame

from snakeySnake.button import Button
from snakeySnake.context import Context
from snakeySnake.screen import Screen

class GameOverScreen(Screen):
    def __init__(self, context: Context):
        super().__init__(context)

        font = pygame.font.Font('freesansbold.ttf', 32)
        self._text = font.render('Game Over', 
                                 True, 
                                 "grey")
        self._textRect = self._text.get_rect()
        self._textRect.center = (int(self._context.getDisplaySize()/2), int(self._context.getDisplaySize()/3))

        self._startButton = Button(self._context.getDisplay(), 
                                   2 * self._context.getDisplaySize()/3, 
                                   2 * self._context.getDisplaySize()/3, 
                                   "Back to Home",
                                   20,
                                   self._context.screenToStart)
        self._gameButton = Button(self._context.getDisplay(), 
                                  self._context.getDisplaySize()/3, 
                                  2 * self._context.getDisplaySize()/3, 
                                  "Try Again",
                                  20,
                                  self._context.screenToGame)
    def draw(self):
        """Displays the game over screen"""

        self._context.getDisplay().blit(self._text, self._textRect)
        self._context.getScoreBoard().displayPastScores()
        self._startButton.process()
        self._gameButton.process()