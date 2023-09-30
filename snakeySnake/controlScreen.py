import pygame

from snakeySnake.button import Button

class ControlScreen:
    def __init__(self, display: pygame.Surface, screenCallback):
        self._display = display
        self._displaySize = self._display.get_width()

        font = pygame.font.Font('freesansbold.ttf', 32)
        self._title = font.render('Controls', 
                           True, 
                           "grey")
        self._titleRect = self._title.get_rect()
        self._titleRect.center = (self._displaySize/2, self._displaySize/3)
        self._textBuffer = 40
        

        font = pygame.font.Font('freesansbold.ttf', 20)
        textStrings = ["- Move your snake using 'ASWD' or the arrow keys",
                       "- Collect",
                       "- Don't run into yourself or the walls",
                       "Good Luck!"]
        self._textRects = []
        self._textStrings = []
        buffer = self._textBuffer
        for line in textStrings:
            text = font.render(line, 
                               True, 
                               "white")
            textRect = text.get_rect()
            textRect.center = (self._displaySize/2, self._displaySize/3 + buffer)
            self._textStrings.append(text)
            self._textRects.append(textRect)
            buffer += self._textBuffer
        
        self._startButton = Button(self._display, 
                         self._displaySize/2, 
                         2 * self._displaySize/3, 
                         "Back to Home",
                         20,
                         screenCallback)

    def draw(self):
        """Displays the controls for the snake game"""

        self._display.fill("black")
        self._display.blit(self._title, self._titleRect)
        
        for idx in range(len(self._textStrings)):
            self._display.blit(self._textStrings[idx], self._textRects[idx])

            # if line == "- Collect":
            #     self._display.blit(self._appleImage, (textRect.right + 2, textRect.top - 8))
        
        
        self._startButton.process()