from snake import Snake
from scoreboard import ScoreBoard
import time
import random

import pygame

class Game:
    def __init__(self):
        self.displaySize = 600

        self.snake = Snake(self.displaySize/2)
        self.scoreBoard = ScoreBoard()
        self.lastUpdateTime = time.perf_counter()
        self.lastAppleTime = time.perf_counter()

        self.appleLocations = []
        self.gameOver = False
        self.exit = False

    def run(self):
        # Initialise board
        pygame.init()
        display = pygame.display.set_mode((self.displaySize, self.displaySize))
        pygame.display.update()
        pygame.display.set_caption('Snake Game')

        while (not self.exit):
            for event in pygame.event.get():
                # Quit game
                if (event.type == pygame.QUIT):
                    self.exit = True

            while (not self.gameOver):
                for event in pygame.event.get():
                    # Move snake based on key movements
                    if (event.type == pygame.KEYDOWN):
                        xMove = 0
                        yMove = 0
                        if ((event.key == pygame.K_w) or
                            (event.key == pygame.K_UP)):
                            yMove = -1
                        elif ((event.key == pygame.K_s) or
                            (event.key == pygame.K_DOWN)):
                            yMove = 1
                        elif ((event.key == pygame.K_a) or
                            (event.key == pygame.K_LEFT)):
                            xMove = -1
                        elif ((event.key == pygame.K_d) or
                            (event.key == pygame.K_RIGHT)):
                            xMove = 1
                
                        self.snake.move(xMove, yMove)
            
                # Move in direction of travel
                if time.perf_counter() - self.lastUpdateTime > 0.1:
                    self.scoreBoard.addTimeSurvived(time.perf_counter() - self.lastUpdateTime)
                    self.lastUpdateTime = time.perf_counter()
                    self.snake.update()
                    if self.snake.collectedApple(self.appleLocations):
                        self.scoreBoard.appleCollected()
                        self.snake.addToTail()

                display.fill(self.snake.black)
                for apple in self.appleLocations:
                        pygame.draw.circle(display, 
                                           self.snake.red, 
                                           (apple[0],
                                            apple[1]),
                                           self.snake.size)

                if time.perf_counter() - self.lastAppleTime > 5.0:
                    self.lastAppleTime = time.perf_counter()
                    apple = (random.randint(0, self.displaySize),
                            random.randint(0, self.displaySize))
                    self.appleLocations.append(apple)
                
                self.snake.draw(display)
                self.scoreBoard.displayCurrentScore(display)
                self.checkGameOver(display)
                pygame.display.update()
        
        pygame.quit()
        quit()
    
    def checkGameOver(self, display):
        x = self.snake.getHeadX()
        y = self.snake.getHeadY()

        if (x >= self.displaySize or
            x <= 0 or
            y >= self.displaySize or
            y <= 0 or
            self.snake.ranIntoItself()):

            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render('Game Over', 
                               True, 
                               self.snake.white)
            textRect = text.get_rect()
            textRect.center = [self.displaySize/2, self.displaySize/3]
            display.blit(text, textRect)

            self.scoreBoard.writeToFile()
            self.scoreBoard.displayPastScores(display)
            self.gameOver = True
