import pygame

from snakeySnake.button import Button
from snakeySnake.context import Context
from snakeySnake.screen import Screen

class StartScreen(Screen):
    def __init__(self, context: Context):
        super().__init__(context)

        font = pygame.font.Font('freesansbold.ttf', 60)
        self._text = font.render('SnakeySnake', 
                            True, 
                            "white")
        self._textRect = self._text.get_rect()
        self._textRect.center = (int(self._context.getDisplaySize()/2), int(self._context.getDisplaySize()/2))

        self._controlsButton = Button(self._context.getDisplay(), 
                                      5 * self._context.getDisplaySize()/6, 
                                      self._context.getDisplaySize()/14, 
                                      "Controls",
                                      20,
                                      self._context.screenToControls)
        self._snakeDesignButton = Button(self._context.getDisplay(), 
                                         self._context.getDisplaySize()/6, 
                                         2 * self._context.getDisplaySize()/3, 
                                         "Snake Design",
                                         20,
                                         self._context.screenToSnakeDesign)
        self._startButton = Button(self._context.getDisplay(), 
                                   self._context.getDisplaySize()/2, 
                                   2 * self._context.getDisplaySize()/3, 
                                   "Start Game",
                                   20,
                                   self._context.screenToGame)
        self._scoreBoardButton = Button(self._context.getDisplay(), 
                                        5 * self._context.getDisplaySize()/6, 
                                        2 * self._context.getDisplaySize()/3, 
                                        "Score Board",
                                        20,
                                        self._context.screenToScoreBoard)

    def draw(self) -> None:
        """Displays the start screen, ready for keyboard events"""

        self._context.getDisplay().fill("black")
        for i in range(0, self._context.getDisplaySize(), int(self._context.getAppleSize() * 4.6)):
            for j in range(0, self._context.getDisplaySize(), int(self._context.getAppleSize() * 4.6)):
                self._context.getDisplay().blit(self._context.getAppleImage(), (i, j))

        self._context.getDisplay().blit(self._text, self._textRect)
        self._controlsButton.process()
        self._snakeDesignButton.process()
        self._startButton.process()
        self._scoreBoardButton.process()