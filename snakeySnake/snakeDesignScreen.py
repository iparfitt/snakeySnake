import colorsys
import math
import pygame

from snakeySnake.button import Button
from snakeySnake.context import Context
from snakeySnake.screen import Screen

class SnakeDesignScreen(Screen):
    def __init__(self, context: Context) -> None:
        """Initialises a snake design screen
        Args:
            context (Context): A context object containing game data
        """
        super().__init__(context)

        self._defaultColour = (211, 211, 211)
        self._snakeDesign = [self._defaultColour]
        self._designLength = len(self._snakeDesign)
        self._selectedColour = self._defaultColour

        # Initialise text
        font = pygame.font.Font('freesansbold.ttf', 32)
        self._text = font.render('Snake Design', 
                                 True, 
                                 "grey")
        self._textRect = self._text.get_rect()
        self._textRect.center = (int(self._context.getDisplaySize()/2), int(self._context.getDisplaySize()/6))
        self._wheelRect = self._context.getColourWheelImage().get_rect()
        self._wheelRect.center = (int(self._context.getDisplaySize()/2), int(5 * self._context.getDisplaySize()/12))

        # Initialise save button
        self._saveButton = Button(self._context.getDisplay(), 
                                  self._context.getDisplaySize()/2, 
                                  7 * self._context.getDisplaySize()/8, 
                                  "Save",
                                  20,
                                  self._saveSnakeDesign)

    def draw(self, events: list) -> None:
        """Displays the snake design screen, ready for keyboard events
        Args:
            events (list): A list of pygame events
        """
        
        self._context.getDisplay().fill("black")
        self._context.getDisplay().blit(self._text, self._textRect)
        self._context.getDisplay().blit(self._context.getColourWheelImage(), self._wheelRect)
        
        self._designLength = len(self._snakeDesign)
        for idx in range(self._designLength):
            pygame.draw.rect(self._context.getDisplay(), 
                             self._snakeDesign[idx],
                             [(self._context.getDisplaySize()/2 + self._context.getSnakeSize() * (2 * idx - self._designLength),
                               3 * self._context.getDisplaySize()/4),
                              (2 * self._context.getSnakeSize(),
                               2 * self._context.getSnakeSize())],
                             border_radius = int(self._context.getSnakeSize()/4))

        mousePos = pygame.mouse.get_pos() 
        distance = math.hypot(self._wheelRect.centerx - mousePos[0], self._wheelRect.centery - mousePos[1])
        if distance <= self._context.getColourWheelRadius():
            for event in events:
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    angle = math.atan2(mousePos[0] - self._wheelRect.centerx, mousePos[1] - self._wheelRect.centery)
                    if angle < 0:
                        angle += 2 * math.pi

                    rgb = colorsys.hsv_to_rgb(angle  / (2 * math.pi),
                                              distance / self._context.getColourWheelRadius(),
                                              1)
                    rgb = tuple(int(i * 255) for i in rgb)
                    self._snakeDesign[-1] = rgb
            
        if (self._designLength < 5):
            self._plusButton = Button(self._context.getDisplay(),
                                      self._context.getDisplaySize()/2 + self._context.getSnakeSize() * (self._designLength + 1/2),
                                      3 * self._context.getDisplaySize()/4 + self._context.getSnakeSize()/2, 
                                      "+",
                                      15,
                                      self._addToSnakeDesign)
            self._plusButton.process(events)
        if (self._designLength > 1):
            self._minusButton = Button(self._context.getDisplay(), 
                                       self._context.getDisplaySize()/2 + self._context.getSnakeSize() * (self._designLength + 1/2),
                                       3 * self._context.getDisplaySize()/4 + 5*self._context.getSnakeSize()/4, 
                                       "-",
                                       15,
                                       self._removeFromSnakeDesign)
            self._minusButton.process(events)
        
        self._saveButton.process(events)
    
    def _addToSnakeDesign(self) -> None:
        """Add an element to the snake design"""
        self._snakeDesign.append(self._defaultColour)
    
    def _removeFromSnakeDesign(self) -> None:
        """Remove the back element from the snake design"""
        self._snakeDesign.pop(-1)
    
    def _saveSnakeDesign(self) -> None:
        """Saves the snake design"""
        self._context.saveSnakeDesign(self._snakeDesign)
        self._snakeDesign = [self._defaultColour]
        self._selectedColour = self._defaultColour
        self._context.screenToStart()