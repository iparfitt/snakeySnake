import pygame

from snakeySnake.button import Button
from snakeySnake.context import Context
from snakeySnake.screen import Screen

class ControlScreen(Screen):
    def __init__(self, context: Context):
        super().__init__(context)
        self._display = self._context.getDisplay()

        font = pygame.font.Font('freesansbold.ttf', 32)
        self._title = font.render('Controls', 
                                  True, 
                                  "grey")
        self._titleRect = self._title.get_rect()
        self._titleRect.center = (int(self._context.getDisplaySize()/2), int(self._context.getDisplaySize()/3))
        self._textBuffer = 40
        
        font = pygame.font.Font('freesansbold.ttf', 20)
        self._textStrings = ["- Move your snake using 'ASWD' or the arrow keys",
                             "- Collect",
                             "- Don't run into yourself or the walls",
                             "Good Luck!"]
        self._textRects = []
        self._textSurfaces = []
        buffer = self._textBuffer
        for line in self._textStrings:
            text = font.render(line, 
                               True, 
                               "white")
            textRect = text.get_rect()
            textRect.center = (int(self._context.getDisplaySize()/2), int(self._context.getDisplaySize()/3 + buffer))
            self._textSurfaces.append(text)
            self._textRects.append(textRect)
            buffer += self._textBuffer
        
        self._startButton = Button(self._context.getDisplay(), 
                                   self._context.getDisplaySize()/2, 
                                   2 * self._context.getDisplaySize()/3, 
                                   "Back to Home",
                                   20,
                                   self._context.screenToStart)

    def draw(self):
        """Displays the controls for the snake game"""

        self._display.fill("black")
        self._display.blit(self._title, self._titleRect)
        
        for idx in range(len(self._textStrings)):
            self._display.blit(self._textSurfaces[idx], self._textRects[idx])

            if self._textStrings[idx] == "- Collect":
                self._display.blit(self._context.getAppleImage(), (self._textRects[idx].right + 2, self._textRects[idx].top - 8))
        
        self._startButton.process()