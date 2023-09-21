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

        self._displaySize = 600
        self._borderWidth = 10
        self._gameSize = self._displaySize - self._borderWidth
        self._fps = 60
        self._fpsClock = pygame.time.Clock()

        # Initialise board
        pygame.init()
        self._display = pygame.display.set_mode((self._displaySize, self._displaySize))
        self._screen = Screen.START
        pygame.display.update()
        pygame.display.set_caption('Snake Game')

        self._scoreBoard = ScoreBoard(self._display)
        self._snake = Snake(self._display,
                           (self._displaySize/2,
                            self._displaySize/2),
                           0.1, 
                           self._scoreBoard.addTimeSurvived, 
                           self._scoreBoard.addAppleCollected)
        self._lastUpdateTime = time.perf_counter()
        self._lastAppleTime = time.perf_counter()

        self._appleSize = self._snake.getSize() * 2
        self._appleLocations = []

        self._appleImage = pygame.image.load(str(pathlib.Path(__file__).parent.absolute()) + "/data/apple.png").convert()
        self._appleImage = pygame.transform.scale(self._appleImage, (self._appleSize, self._appleSize))

        self._gameOver = False
        self._exit = False

    def run(self) -> None:
        """Run the main loop of the game"""

        while (not self._exit):
            for event in pygame.event.get():
                # Quit game
                if (event.type == pygame.QUIT):
                    self._exit = True

            if (self._screen == Screen.START):
                self._startScreen()
            elif (self._screen == Screen.SCOREBOARD):
                self._scoreBoardScreen()
            elif (self._screen == Screen.TUTORIAL):
                self._tutorialScreen()
            elif (self._screen == Screen.GAME):
                self._gameScreen()
            else:
                self._gameOverScreen()
        
            pygame.display.flip()
            self._fpsClock.tick(self._fps)
        
        pygame.quit()
        quit()
    
    def _drawApples(self) -> None:
        """Draw apples in a random location if time since the last apple has elapsed"""

        if time.perf_counter() - self._lastAppleTime > 5.0:
            self._lastAppleTime = time.perf_counter()
            self._appleLocations.extend([(random.randint(self._borderWidth, self._gameSize - self._appleSize),
                                        random.randint(self._borderWidth, self._gameSize - self._appleSize))])

        for apple in self._appleLocations:
            self._display.blit(self._appleImage, apple)

    def _checkGameOver(self) -> None:
        """Runs cleanup if the game is over, including writing the current score to file and resetting the game"""

        x = self._snake.getHeadX()
        y = self._snake.getHeadY()

        if (x >= self._gameSize or
            x <= self._borderWidth or
            y >= self._gameSize or
            y <= self._borderWidth or
            self._snake.ranIntoItself()):

            self._screen = Screen.GAMEOVER
            self._scoreBoard.writeToFile()
            self._snake.reset()
            self._appleLocations.clear()
    
    def _gameScreen(self) -> None:
        """Displays the game screen, ready for keyboard events"""

        while (self._screen == Screen.GAME):
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
                    self._snake.move(direction)
            self._snake.update(self._appleLocations)
            
            self._display.fill("grey")
            pygame.draw.rect(self._display, 
                             "black", 
                             [self._borderWidth, 
                              self._borderWidth, 
                              self._gameSize - self._borderWidth, 
                              self._gameSize - self._borderWidth])

            self._drawApples()
            self._snake.draw()
            self._scoreBoard.displayCurrentScore(self._borderWidth)
            self._checkGameOver()
            pygame.display.flip()
            self._fpsClock.tick(self._fps)

    def _startScreen(self) -> None:
        """Displays the start screen, ready for keyboard events"""

        self._display.fill("black")
        for i in range(0, self._displaySize, int(self._appleSize * 4.6)):
            for j in range(0, self._displaySize, int(self._appleSize * 4.6)):
                self._display.blit(self._appleImage, (i, j))

        font = pygame.font.Font('freesansbold.ttf', 60)
        text = font.render('SnakeySnake', 
                            True, 
                            "white")
        textRect = text.get_rect()
        textRect.center = [self._displaySize/2, self._displaySize/2]
        self._display.blit(text, textRect)
        tutorialButton = Button(self._display, 
                                self._displaySize/6, 
                                2 * self._displaySize/3, 
                                "Tutorial",
                                self._screenToTutorial)
        startButton = Button(self._display, 
                             self._displaySize/2, 
                             2 * self._displaySize/3, 
                             "Start Game",
                             self._screenToGame)
        scoreBoardButton = Button(self._display, 
                                  5 * self._displaySize/6, 
                                  2 * self._displaySize/3, 
                                  "Score Board",
                                  self._screenToScoreBoard)

        startButton.process()
        tutorialButton.process()
        scoreBoardButton.process()

    def _tutorialScreen(self) -> None:
        """Displays a tutorial for the snake game"""

        self._display.fill("black")
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Tutorial', 
                           True, 
                           "grey")
        textRect = text.get_rect()
        textRect.center = [self._displaySize/2, self._displaySize/3]
        self._display.blit(text, textRect)

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
            textRect.center = [self._displaySize/2, self._displaySize/3 + buffer]
            self._display.blit(text, textRect)
            buffer += 40

            if line == "- Collect":
                self._display.blit(self._appleImage, (textRect.right + 2, textRect.top - 8))
        
        startButton = Button(self._display, 
                         self._displaySize/2, 
                         2 * self._displaySize/3, 
                         "Back to Home",
                         self._screenToStart)
        startButton.process()

    def _scoreBoardScreen(self) -> None:
        """Displays the current local scoreboard"""

        self._display.fill("black")
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Score Board', 
                           True, 
                           "grey")
        textRect = text.get_rect()
        textRect.center = [self._displaySize/2, self._displaySize/3]
        self._display.blit(text, textRect)
        self._scoreBoard.displayPastScores()
        startButton = Button(self._display, 
                         self._displaySize/2, 
                         2 * self._displaySize/3, 
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
        textRect.center = [self._displaySize/2, self._displaySize/3]
        self._display.blit(text, textRect)
        self._scoreBoard.displayPastScores()

        startButton = Button(self._display, 
                             2 * self._displaySize/3, 
                             2 * self._displaySize/3, 
                             "Back to Home",
                             self._screenToStart)
        gameButton = Button(self._display, 
                             self._displaySize/3, 
                             2 * self._displaySize/3, 
                             "Try Again",
                             self._screenToGame)
        startButton.process()
        gameButton.process()

    def _screenToStart(self) -> None:
        """Changes the screen to the start screen"""
        self._screen = Screen.START

    def _screenToScoreBoard(self) -> None:
        """Changes the screen to the scoreboard screen"""
        self._screen = Screen.SCOREBOARD
    
    def _screenToTutorial(self) -> None:
        """Changes the screen to the tutorial screen"""
        self._screen = Screen.TUTORIAL
    
    def _screenToGame(self) -> None:
        """Changes the screen to the game screen"""
        self._screen = Screen.GAME
        self._snake.startTimer()
        self._scoreBoard.reset()
    
    def _screenToGameOver(self)-> None:
        """Changes the screen to the game over screen"""
        self._screen = Screen.GAMEOVER
