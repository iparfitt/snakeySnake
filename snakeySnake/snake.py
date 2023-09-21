import pygame
from time import perf_counter as timer

from snakeySnake.enums import Direction

directionMap = {Direction.NONE: (0, 0),
                Direction.LEFT: (-1, 0),
                Direction.RIGHT: (1, 0),
                Direction.UP: (0, -1),
                Direction.DOWN: (0, 1)}

# A class describing the snake and its movements
class Snake():
    def __init__(self, 
                 display: pygame.display, 
                 startingPos: tuple, 
                 updateInterval: float, 
                 addTimeSurvived, 
                 addAppleCollected) -> None:
        """Initialises a snake object

        Args:
            display           (pygame.display): The surface to place the button on
            startingPos       (tuple): The starting coord of the snake
            updateInterval    (float): The interval to update the snake's movements on
            addTimeSurvived   (function(float)): A function to call when additional time is survived
            addAppleCollected (function(None)): A function to call when an apple is collected
        """
        self.display = display
        self.size = 20
        
        self.body = [pygame.Rect(startingPos,  
                                 (self.size, 
                                  self.size))]
        self.startingHead = self.body[0]

        self.bodyLen = 1
        self.directionName = Direction.RIGHT
        self.direction = directionMap[self.directionName] # Initially moving right

        self.lastUpdateTime = timer()
        self.updateInterval = updateInterval
        self.addTimeSurvived = addTimeSurvived
        self.addAppleCollected = addAppleCollected
    
    def move(self, 
             directionName: Direction) -> None:
        """Move the snake in the specified direction

        Args:
            direction (Direction): The direction to move the snake in
        """
        self.directionName = directionName
        self.direction = directionMap[directionName]
        self._shift(self.direction[0], self.direction[1])
        
    def update(self, 
               appleLocations: list) -> None:
        """Update the snake object by moving 1 pixel in the direction of travel

        Args:
            appleLocations (list(tuple)): The locations of apples on the board
        """
        # Move in direction of travel
        if timer() - self.lastUpdateTime > self.updateInterval:
            self.addTimeSurvived(timer() - self.lastUpdateTime)
            self.lastUpdateTime = timer()
            self._checkIfCollectedApple(appleLocations)

            # Move snake 1 pixel in the direction of travel
            self._shift(self.direction[0], self.direction[1])
    
    def draw(self) -> None:
        """Draw the snake on the screen"""

        for idx in range(self.bodyLen):
            if idx % 2 == 1:
                pygame.draw.rect(self.display, "yellow", self.body[idx])
            else:
                pygame.draw.rect(self.display, "green", self.body[idx])

    def ranIntoItself(self) -> bool:
        """Returns true if the snake has run into itself, false otherwise""" 
        for idx in range(2, self.bodyLen):
            if (self.getHeadX() == self.body[idx].x and 
                self.getHeadY() == self.body[idx].y):
                return True
        return False
    
    def reset(self) -> None:
        """Resets the snake to its starting location and size"""
        self.body = [self.startingHead]
        self.bodyLen = 1
        self.directionName = Direction.RIGHT
        self.direction = directionMap[self.directionName]
    
    def getHeadX(self) -> float:
        """Returns the current x coordinate of the head"""
        return self.body[0].x

    def getHeadY(self) -> float:
        """Returns the curent y coordinate of the head"""
        return self.body[0].y
    
    def _shift(self, xMove, yMove) -> None:
        """Shifts every pixel to the location of the pixel ahead"""

        # Every pixel moves to position of pixel ahead, except head
        for idx in range(self.bodyLen - 1, 0, -1):
            self.body[idx] = self.body[idx - 1]

        # Move head
        self.body[0] = self.body[0].move(xMove * self.size, 
                                         yMove * self.size)
    
    def _addToTail(self) -> None:
        """Adds a pixel to the tail of the snake"""

        self.body.append(self.body[self.bodyLen - 1])
        self.bodyLen += 1
        self.body[self.bodyLen - 1].move(self.direction[0] * -self.size,
                                         self.direction[1] * -self.size)

    def _checkIfCollectedApple(self, 
                               appleLocations: list) -> None:
        """Checks if the snake has collected an apple, and adds to the tail if it has
        
        Args:
            appleLocations (list(tuple)): The locations of all apples on the screen
        """
        for apple in appleLocations:
            if (abs(self.getHeadX() - apple[0]) <= 2 * self.size and 
                abs(self.getHeadY() - apple[1]) <= 2 * self.size):
                appleLocations.remove(apple)
                self.addAppleCollected()
                self._addToTail()
