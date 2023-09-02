import pygame

class Snake():
    def __init__(self, startingPos):
        self.blue = (0,0,255)
        self.red = (255,0,0)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.size = 20
        self.body = [pygame.Rect(startingPos, 
                                 startingPos, 
                                 self.size, 
                                 self.size)]
        self.bodyLen = 1
        self.headX = startingPos
        self.headY = startingPos
        self.direction = [1, 0] # Initially moving right
    
    # Update snake direction
    def move(self, xMove, yMove):
        self.direction = [xMove, yMove]
        self._shift(xMove, yMove)
        
    # Shift snake 1 pixel in the direction of travel
    def update(self):
        # Move snake 1 pixel in the direction of travel
        self._shift(self.direction[0], self.direction[1])
    
    # Add extra pixel to snake
    def addToTail(self):
        self.body.append(self.body[self.bodyLen - 1])
        self.bodyLen += 1
        self.body[self.bodyLen - 1].move(self.direction[0] * -self.size,
                                         self.direction[1] * -self.size)

    # Draw snake, return true if updated, false if game over
    def draw(self, display) -> bool:
        for pixel in self.body:
            pygame.draw.rect(display, self.blue, pixel)

    def collectedApple(self, appleLocations) -> bool:
        for apple in appleLocations:
            if (abs(self.getHeadX() - apple[0]) <= 2 * self.size and 
                abs(self.getHeadY() - apple[1]) <= 2 * self.size):
                appleLocations.remove(apple)
                return True
        return False

    def ranIntoItself(self) -> bool:
        if self.bodyLen < 4:
            return False
        
        for idx in range(2, self.bodyLen):
            if (self.getHeadX() == self.body[idx].x and 
                self.getHeadY() == self.body[idx].y):
                return True
        return False
    
    def getHeadX(self):
        return self.body[0].x

    def getHeadY(self):
        return self.body[0].y
    
    def _shift(self, xMove, yMove):
        # Every pixel moves to position of pixel ahead, except head
        for idx in range(self.bodyLen - 1, 0, -1):
            self.body[idx] = self.body[idx - 1]

        # Move head
        self.body[0] = self.body[0].move(xMove * self.size, 
                                         yMove * self.size)
