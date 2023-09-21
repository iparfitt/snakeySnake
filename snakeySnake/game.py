import time
import random
import pygame
import pathlib

from snakeySnake.enums import Direction, Screen
from snakeySnake.snake import Snake
from snakeySnake.scoreboard import ScoreBoard
from snakeySnake.button import Button

# The main class describing a snake game
class Game:
    def __init__(self) -> None:
        """Initialises a game object"""

        self.displaySize = 600
        self.borderWidth = 10
        self.gameSize = self.displaySize - self.borderWidth
        self.fps = 60
        self.fpsClock = pygame.time.Clock()

        # Initialise board
        pygame.init()
        self.display = pygame.display.set_mode((self.displaySize, self.displaySize))
        self.screen = Screen.START
        pygame.display.update()
        pygame.display.set_caption('Snake Game')

        self.scoreBoard = ScoreBoard(self.display)
        self.snake = Snake(self.display,
                           (self.displaySize/2,
                            self.displaySize/2),
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

    def run(self) -> None:
        """Run the main loop of the game"""

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
        
            pygame.display.flip()
            self.fpsClock.tick(self.fps)
        
        pygame.quit()
        quit()
    
    def _drawApples(self) -> None:
        """Draw apples in a random location if time since the last apple has elapsed"""

        if time.perf_counter() - self.lastAppleTime > 5.0:
            self.lastAppleTime = time.perf_counter()
            self.appleLocations.extend([(random.randint(self.borderWidth, self.gameSize - self.appleSize),
                                        random.randint(self.borderWidth, self.gameSize - self.appleSize))])

        for apple in self.appleLocations:
            self.display.blit(self.appleImage, apple)

    def _checkGameOver(self) -> None:
        """Runs cleanup if the game is over, including writing the current score to file and resetting the game"""

        x = self.snake.getHeadX()
        y = self.snake.getHeadY()

        if (x >= self.gameSize or
            x <= self.borderWidth or
            y >= self.gameSize or
            y <= self.borderWidth or
            self.snake.ranIntoItself()):

            self.screen = Screen.GAMEOVER
            self.scoreBoard.writeToFile()
            self.snake.reset()
            self.appleLocations.clear()
    
    def _gameScreen(self) -> None:
        """Displays the game screen, ready for keyboard events"""

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
            
            self.display.fill("grey")
            pygame.draw.rect(self.display, 
                             "black", 
                             [self.borderWidth, 
                              self.borderWidth, 
                              self.gameSize - self.borderWidth, 
                              self.gameSize - self.borderWidth])

            self._drawApples()
            self.snake.draw()
            self.scoreBoard.displayCurrentScore(self.borderWidth)
            self._checkGameOver()
            pygame.display.flip()
            self.fpsClock.tick(self.fps)

    def _startScreen(self) -> None:
        """Displays the start screen, ready for keyboard events"""

        self.display.fill("black")
        for i in range(0, self.displaySize, int(self.appleSize * 4.6)):
            for j in range(0, self.displaySize, int(self.appleSize * 4.6)):
                self.display.blit(self.appleImage, (i, j))

        font = pygame.font.Font('freesansbold.ttf', 60)
        text = font.render('SnakeySnake', 
                            True, 
                            "white")
        textRect = text.get_rect()
        textRect.center = [self.displaySize/2, self.displaySize/2]
        self.display.blit(text, textRect)
        tutorialButton = Button(self.display, 
                                self.displaySize/6, 
                                2 * self.displaySize/3, 
                                "Tutorial",
                                self._screenToTutorial)
        startButton = Button(self.display, 
                             self.displaySize/2, 
                             2 * self.displaySize/3, 
                             "Start Game",
                             self._screenToGame)
        scoreBoardButton = Button(self.display, 
                                  5 * self.displaySize/6, 
                                  2 * self.displaySize/3, 
                                  "Score Board",
                                  self._screenToScoreBoard)

        startButton.process()
        tutorialButton.process()
        scoreBoardButton.process()

    def _tutorialScreen(self) -> None:
        """Displays a tutorial for the snake game"""

        self.display.fill("black")
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Tutorial', 
                           True, 
                           "grey")
        textRect = text.get_rect()
        textRect.center = [self.displaySize/2, self.displaySize/3]
        self.display.blit(text, textRect)

        font = pygame.font.Font('freesansbold.ttf', 20)
        textStrings = ["- Move your snake using 'ASWD' or the arrow keys",
                       "- Collect",
                       "- Don't run into yourself or the walls",
                       "Good Luck!"]
        
        buffer = 40
        for line in textStrings:
            text = font.render(line, 
                               True, 
                               "white")
            textRect = text.get_rect()
            textRect.center = [self.displaySize/2, self.displaySize/3 + buffer]
            self.display.blit(text, textRect)
            buffer += 40

            if line == "- Collect":
                self.display.blit(self.appleImage, (textRect.right + 2, textRect.top - 8))
        
        startButton = Button(self.display, 
                         self.displaySize/2, 
                         2 * self.displaySize/3, 
                         "Back to Home",
                         self._screenToStart)
        startButton.process()

    def _scoreBoardScreen(self) -> None:
        """Displays the current local scoreboard"""

        self.display.fill("black")
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Score Board', 
                           True, 
                           "grey")
        textRect = text.get_rect()
        textRect.center = [self.displaySize/2, self.displaySize/3]
        self.display.blit(text, textRect)
        self.scoreBoard.displayPastScores()
        startButton = Button(self.display, 
                         self.displaySize/2, 
                         2 * self.displaySize/3, 
                         "Back to Home",
                         self._screenToStart)
        startButton.process()
    
    def _gameOverScreen(self):
        """Displays the game over screen"""

        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Game Over', 
                           True, 
                           "grey")
        textRect = text.get_rect()
        textRect.center = [self.displaySize/2, self.displaySize/3]
        self.display.blit(text, textRect)
        self.scoreBoard.displayPastScores()

        startButton = Button(self.display, 
                             self.displaySize/2, 
                             2 * self.displaySize/3, 
                             "Back to Home",
                             self._screenToStart)
        startButton.process()

    def _screenToStart(self) -> None:
        """Changes the screen to the start screen"""
        self.screen = Screen.START

    def _screenToScoreBoard(self) -> None:
        """Changes the screen to the scoreboard screen"""
        self.screen = Screen.SCOREBOARD
    
    def _screenToTutorial(self) -> None:
        """Changes the screen to the tutorial screen"""
        self.screen = Screen.TUTORIAL
    
    def _screenToGame(self) -> None:
        """Changes the screen to the game screen"""
        self.screen = Screen.GAME
    
    def _screenToGameOver(self)-> None:
        """Changes the screen to the game over screen"""
        self.screen = Screen.GAMEOVER
