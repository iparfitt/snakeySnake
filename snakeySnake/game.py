import time
import random
import pygame
import pathlib

from snakeySnake.enums import Direction, Screen
from snakeySnake.snake import Snake
from snakeySnake.scoreboard import ScoreBoard

class Button:
    def __init__(self, display, x, y, text, onClick):
        font = pygame.font.Font('freesansbold.ttf', 20)
        self.text = font.render(text, 
                                True, 
                                "white")
        self.textRect = self.text.get_rect()
        self.textRect.center = [display.get_width()/3, display.get_height()/4]

        self.onClick = onClick
        
        pygame.draw.rect(display, "grey", 20, )
        display.blit(self.text, self.textRect)
    
    def process(self):
        if (self._isPressed()):
            self.onClick()
    
    def _isPressed(self):
        pass

class Game:
    def __init__(self):
        self.displaySize = 600

        # Initialise board
        pygame.init()
        self.display = pygame.display.set_mode((self.displaySize, self.displaySize))
        self.screen = Screen.START
        pygame.display.update()
        pygame.display.set_caption('Snake Game')

        self.scoreBoard = ScoreBoard()
        self.snake = Snake(self.displaySize/2, 
                           0.1, 
                           self.scoreBoard.addTimeSurvived, 
                           self.scoreBoard.addAppleCollected)
        self.lastUpdateTime = time.perf_counter()
        self.lastAppleTime = time.perf_counter()

        self.appleSize = self.snake.size * 2
        self.appleLocations = []

        self.appleImage = pygame.image.load(str(pathlib.Path(__file__).parent.absolute()) + "/data/apple.png").convert()
        self.appleImage = pygame.transform.scale(self.appleImage, (self.appleSize, self.appleSize))

        self.gameOver = False
        self.exit = False

    def run(self):
        while (not self.exit):
            for event in pygame.event.get():
                # Quit game
                if (event.type == pygame.QUIT):
                    self.exit = True

            if (self.screen == Screen.START):
                self._startScreen()
            elif (self.screen == Screen.SCOREBOARD):
                self._scoreBoardScreen()
            elif (self.screen == Screen.TUTORIAL):
                self._tutorialScreen()
            elif (self.screen == Screen.GAME):
                self._gameScreen()
            else:
                self._gameOverScreen()
        
            pygame.display.update()
        
        pygame.quit()
        quit()
    
    def _drawApples(self):
        if time.perf_counter() - self.lastAppleTime > 5.0:
            self.lastAppleTime = time.perf_counter()
            self.appleLocations.append((random.randint(0, self.displaySize - self.appleSize),
                                        random.randint(0, self.displaySize - self.appleSize)))

        for apple in self.appleLocations:
            self.display.blit(self.appleImage, apple)

    def _checkGameOver(self):
        x = self.snake.getHeadX()
        y = self.snake.getHeadY()

        if (x >= self.displaySize or
            x <= 0 or
            y >= self.displaySize or
            y <= 0 or
            self.snake.ranIntoItself()):

            self.screen = Screen.GAMEOVER
    
    def _gameScreen(self):
        while (self.screen == Screen.GAME):
            for event in pygame.event.get():
                # Move snake based on key movements
                if (event.type == pygame.KEYDOWN):
                    direction = Direction.NONE
                    if ((event.key == pygame.K_w) or
                        (event.key == pygame.K_UP)):
                        direction = Direction.UP
                    elif ((event.key == pygame.K_s) or
                        (event.key == pygame.K_DOWN)):
                        direction = Direction.DOWN
                    elif ((event.key == pygame.K_a) or
                        (event.key == pygame.K_LEFT)):
                        direction = Direction.LEFT
                    elif ((event.key == pygame.K_d) or
                        (event.key == pygame.K_RIGHT)):
                        direction = Direction.RIGHT
                
                    self.snake.move(direction)
                self.snake.update(self.appleLocations)

            self.display.fill("black")
            self._drawApples(self.display, self.appleImage)
            self.snake.draw(self.display)
            self.scoreBoard.displayCurrentScore(self.display)
            self._checkGameOver(self.display)
            pygame.display.update()

    def _tutorialScreen(self):
        self.display.fill("black")
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Tutorial', 
                           True, 
                           "white")
        textRect = text.get_rect()
        textRect.center = [self.displaySize/2, self.displaySize/3]
        self.display.blit(text, textRect)

    def _startScreen(self):
        while (self.screen == Screen.START):
            self.display.fill("black")

            for i in range(0, self.displaySize, self.appleSize * 2):
                for j in range(0, self.displaySize, self.appleSize * 2):
                    self.display.blit(self.appleImage, (i, j))

            font = pygame.font.Font('freesansbold.ttf', 50)
            text = font.render('SnakeySnake', 
                                True, 
                                "white")
            textRect = text.get_rect()
            textRect.center = [self.displaySize/2, self.displaySize/2]
            self.display.blit(text, textRect)

            startButton = Button(self.display, 
                                 self.displaySize/4, 
                                 self.displaySize/3, 
                                 "Start Game",
                                 self.screen,
                                 Screen.GAME)
            tutorialButton = Button(self.display, 
                                    self.displaySize/2, 
                                    self.displaySize/3, 
                                    "Start Game")
            scoreBoardButton = Button(self.display, 
                                      3 * self.displaySize/4, 
                                      self.displaySize/3, 
                                      "Score Board")
            
            startButton.process()
            tutorialButton.process()
            scoreBoardButton.process()

    def _scoreBoardScreen(self):
        self.display.fill("black")
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Scoreboard', 
                           True, 
                           "white")
        textRect = text.get_rect()
        textRect.center = [self.displaySize/2, self.displaySize/3]
        self.display.blit(text, textRect)
        self.scoreBoard.displayPastScores(self.display)
    
    def _gameOverScreen(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Game Over', 
                           True, 
                           "white")
        textRect = text.get_rect()
        textRect.center = [self.displaySize/2, self.displaySize/3]
        self.display.blit(text, textRect)
        self.scoreBoard.writeToFile()
        self.scoreBoard.displayPastScores(self.display)
