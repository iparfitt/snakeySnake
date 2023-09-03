import pygame

directionMap = {"Left": (-1, 0),
                "Right": (1, 0),
                "Up": (0, -1),
                "Down": (0, 1)}
class Snake():
    def __init__(self, startingPos):
        self.size = 20
        self.body = [pygame.Rect(startingPos, 
                                 startingPos, 
                                 self.size, 
                                 self.size)]
        self.bodyLen = 1
        self.headX = startingPos
        self.headY = startingPos
        self.directionName = "Right"
        self.direction = directionMap[self.directionName] # Initially moving right
    
    # Update snake direction
    def move(self, directionName):
        self.directionName = directionName
        self.direction = directionMap[directionName]
        self._shift(self.direction[0], self.direction[1])
        
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
        for idx in range(1, self.bodyLen):
            if idx % 2 == 1:
                pygame.draw.rect(display, "yellow", self.body[idx])
            else:
                pygame.draw.rect(display, "green", self.body[idx])
        
        radius = int(self.size/2)
        topLeft = (self.directionName == "Left" or 
                   self.directionName == "Up") * radius
        topRight = (self.directionName == "Right" or 
                    self.directionName == "Up") * radius
        bottomLeft = (self.directionName == "Left" or 
                      self.directionName == "Down") * radius
        bottomRight = (self.directionName == "Right" or 
                       self.directionName == "Down") * radius
        pygame.draw.rect(display, 
                         "green", 
                         self.body[0], 
                         0, 
                         radius,
                         topLeft,
                         topRight,
                         bottomLeft,
                         bottomRight)

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
