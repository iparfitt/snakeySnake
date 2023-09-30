import pygame
from time import perf_counter as timer

from snakeySnake.enums import Direction

directionMap = {Direction.NONE:  (0, 0),
                Direction.LEFT:  (-1, 0),
                Direction.RIGHT: (1, 0),
                Direction.UP:    (0, -1),
                Direction.DOWN:  (0, 1)}

# A class describing the snake and its movements
class Snake():
    def __init__(self, 
                 display: pygame.Surface, 
                 startingPos: tuple, 
                 updateInterval: float, 
                 addTimeSurvived, 
                 addAppleCollected) -> None:
        """Initialises a snake object

        Args:
            display           (pygame.Surface): The surface to place the button on
            startingPos       (tuple): The starting coord of the snake
            updateInterval    (float): The interval to update the snake's movements on
            addTimeSurvived   (function(float)): A function to call when additional time is survived
            addAppleCollected (function(None)): A function to call when an apple is collected
        """
        self._display = display
        self._size = 20
        self._tongueWidth = self._size/2
        
        self._body = [pygame.Rect(startingPos,  
                                 (self._size, 
                                  self._size))]
        self._startingHead = self._body[0]
        self._snakeDesign = ['#4CFF33']
        self._numColours = len(self._snakeDesign)

        self._bodyLen = 1
        self._directionName = Direction.RIGHT
        self._direction = directionMap[self._directionName] # Initially moving right

        self._lastUpdateTime = timer()
        self._updateInterval = updateInterval
        self._addTimeSurvived = addTimeSurvived
        self._addAppleCollected = addAppleCollected
    
    def getSize(self) -> float:
        """Returns the size of a pixel of the snake"""
        return self._size
    
    def move(self, 
             directionName: Direction) -> None:
        """Move the snake in the specified direction

        Args:
            direction (Direction): The direction to move the snake in
        """
        self._directionName = directionName
        self._direction = directionMap[directionName]
        self._shift(self._direction[0], self._direction[1])
        
    def update(self, 
               appleLocations: list) -> None:
        """Update the snake object by moving 1 pixel in the direction of travel

        Args:
            appleLocations (list(tuple)): The locations of apples on the board
        """
        # Move in direction of travel
        if timer() - self._lastUpdateTime > self._updateInterval:
            self._addTimeSurvived(timer() - self._lastUpdateTime)
            self._lastUpdateTime = timer()
            self._checkIfCollectedApple(appleLocations)

            # Move snake 1 pixel in the direction of travel
            self._shift(self._direction[0], self._direction[1])
    
    def startTimer(self) -> None:
        """Update the timer"""
        self._lastUpdateTime = timer()

    def draw(self) -> None:
        """Draw the snake on the screen"""
        for idx in range(self._bodyLen - 1, -1, -1):
            pygame.draw.rect(self._display, 
                             self._snakeDesign[idx % self._numColours], 
                             self._body[idx], 
                             border_radius = int(self._size/4))

    def ranIntoItself(self) -> bool:
        """Returns true if the snake has run into itself, false otherwise""" 

        for idx in range(2, self._bodyLen):
            if (self.getHeadX() == self._body[idx].x and 
                self.getHeadY() == self._body[idx].y):
                return True
        return False
    
    def saveDesign(self, snakeDesign) -> None:
        """Set the snake design"""
        self._snakeDesign = snakeDesign
        self._numColours = len(self._snakeDesign)
    
    def reset(self) -> None:
        """Resets the snake to its starting location and size"""

        self._body = [self._startingHead]
        self._bodyLen = 1
        self._directionName = Direction.RIGHT
        self._direction = directionMap[self._directionName]
    
    def getHeadX(self) -> float:
        """Returns the current x coordinate of the head"""
        return self._body[0].x

    def getHeadY(self) -> float:
        """Returns the curent y coordinate of the head"""
        return self._body[0].y
    
    def _shift(self, xMove, yMove) -> None:
        """Shifts every pixel to the location of the pixel ahead"""

        # Every pixel moves to position of pixel ahead, except head
        for idx in range(self._bodyLen - 1, 0, -1):
            self._body[idx] = self._body[idx - 1]

        # Move head
        self._body[0] = self._body[0].move(xMove * 2 * self._size/3, 
                                           yMove * 2 * self._size/3)
    
    def _addToTail(self) -> None:
        """Adds a pixel to the tail of the snake"""

        self._body.append(self._body[self._bodyLen - 1])
        self._bodyLen += 1
        self._body[self._bodyLen - 1].move(self._direction[0] * -self._size,
                                           self._direction[1] * -self._size)

    def _checkIfCollectedApple(self, 
                               appleLocations: list) -> None:
        """Checks if the snake has collected an apple, and adds to the tail if it has

        Args:
            appleLocations (list(tuple)): The locations of all apples on the screen
        """
        for apple in appleLocations:
            if (abs(self.getHeadX() - apple[0]) <= 2 * self._size and 
                abs(self.getHeadY() - apple[1]) <= 2 * self._size):
                appleLocations.remove(apple)
                self._addAppleCollected()
                self._addToTail()
