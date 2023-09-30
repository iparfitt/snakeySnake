import colorsys
import math
import pathlib
import pygame
import random
import time

from snakeySnake.button import Button
from snakeySnake.enums import Direction, Screen
from snakeySnake.scoreboard import ScoreBoard
from snakeySnake.snake import Snake

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
                           0.05, 
                           self._scoreBoard.addTimeSurvived, 
                           self._scoreBoard.addAppleCollected)
        self._lastUpdateTime = time.perf_counter()
        self._lastAppleTime = time.perf_counter()

        self._appleSize = self._snake.getSize() * 2
        self._appleLocations = []

        self._appleImage = pygame.image.load(str(pathlib.Path(__file__).parent.absolute()) + "/data/apple.png").convert()
        self._appleImage = pygame.transform.scale(self._appleImage, (self._appleSize, self._appleSize))
        
        self._colourWheelRadius = self._snake.getSize() * 5
        self._colourWheelImage = pygame.image.load(str(pathlib.Path(__file__).parent.absolute()) + "/data/colour_wheel.png").convert()
        self._colourWheelImage = pygame.transform.scale(self._colourWheelImage, (self._colourWheelRadius*2, self._colourWheelRadius*2))

        self._snakeDesign = ['#ffffff']
        self._selectedColour = (255, 100, 0)

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
            elif (self._screen == Screen.CONTROLS):
                self._controlsScreen()
            elif (self._screen == Screen.GAME):
                self._gameScreen()
            elif (self._screen == Screen.SNAKEDESIGN):
                self._snakeDesignScreen()
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
        controlsButton = Button(self._display, 
                                5 * self._displaySize/6, 
                                self._displaySize/14, 
                                "Controls",
                                20,
                                self._screenToControls)
        snakeDesignButton = Button(self._display, 
                                   self._displaySize/6, 
                                   2 * self._displaySize/3, 
                                   "Snake Design",
                                   20,
                                   self._screenToSnakeDesign)
        startButton = Button(self._display, 
                             self._displaySize/2, 
                             2 * self._displaySize/3, 
                             "Start Game",
                             20,
                             self._screenToGame)
        scoreBoardButton = Button(self._display, 
                                  5 * self._displaySize/6, 
                                  2 * self._displaySize/3, 
                                  "Score Board",
                                  20,
                                  self._screenToScoreBoard)

        controlsButton.process()
        snakeDesignButton.process()
        startButton.process()
        scoreBoardButton.process()

    def _controlsScreen(self) -> None:
        """Displays the controls for the snake game"""

        self._display.fill("black")
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Controls', 
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
                         20,
                         self._screenToStart)
        startButton.process()

    def _snakeDesignScreen(self) -> None:
        """Displays the snake design screen, ready for keyboard events"""

        self._display.fill("black")
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Snake Design', 
                           True, 
                           "grey")
        textRect = text.get_rect()
        textRect.center = [self._displaySize/2, self._displaySize/6]
        self._display.blit(text, textRect)

        wheelRect = self._colourWheelImage.get_rect()
        wheelRect.center = [self._displaySize/2, 5 * self._displaySize/12]
        self._display.blit(self._colourWheelImage, wheelRect)

        snakeDesignLength = len(self._snakeDesign)
        mousePos = pygame.mouse.get_pos() 
        for idx in range(snakeDesignLength):
            pygame.draw.rect(self._display, 
                             self._snakeDesign[idx],
                             [self._displaySize/2 + self._snake.getSize() * (2 * idx - snakeDesignLength),
                              3 * self._displaySize/4,
                              2 * self._snake.getSize(),
                              2 * self._snake.getSize()],
                             border_radius = int(self._snake.getSize()/4))

        distance = math.hypot(wheelRect.centerx - mousePos[0], wheelRect.centery - mousePos[1])
        if distance <= self._colourWheelRadius:
            for event in pygame.event.get():
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    angle = math.atan2(mousePos[0] - wheelRect.centerx, mousePos[1] - wheelRect.centery)
                    if angle < 0:
                        angle += 2 * math.pi

                    rgb = colorsys.hsv_to_rgb(angle  / (2 * math.pi),
                                              distance / self._colourWheelRadius,
                                              1)
                    rgb = tuple(int(i * 255) for i in rgb)
                    self._snakeDesign[-1] = rgb
            
        if (snakeDesignLength < 5):
            plusButton = Button(self._display,
                                self._displaySize/2 + self._snake.getSize() * (snakeDesignLength + 1/2),
                                3 * self._displaySize/4 + self._snake.getSize()/2, 
                                "+",
                                15,
                                self._addToSnakeDesign)
            plusButton.process()
        if (snakeDesignLength > 1):
            minusButton = Button(self._display, 
                                 self._displaySize/2 + self._snake.getSize() * (snakeDesignLength + 1/2),
                                 3 * self._displaySize/4 + 5*self._snake.getSize()/4, 
                                 "-",
                                 15,
                                 self._removeFromSnakeDesign)
            minusButton.process()
        saveButton = Button(self._display, 
                            self._displaySize/2, 
                            7 * self._displaySize/8, 
                            "Save",
                            20,
                            self._saveSnakeDesign)
        saveButton.process()

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
                             20,
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
                             20,
                             self._screenToStart)
        gameButton = Button(self._display, 
                            self._displaySize/3, 
                            2 * self._displaySize/3, 
                            "Try Again",
                            20,
                            self._screenToGame)
        startButton.process()
        gameButton.process()

    def _screenToStart(self) -> None:
        """Changes the screen to the start screen"""
        self._screen = Screen.START
    
    def _screenToControls(self) -> None:
        """Changes the screen to the controls screen"""
        self._screen = Screen.CONTROLS

    def _screenToSnakeDesign(self) -> None:
        """Changes the screen to the snake design screen"""
        self._screen = Screen.SNAKEDESIGN
        self._snakeDesign = ['#ffffff']
        self._selectedColour = (255, 100, 0)
    
    def _screenToGame(self) -> None:
        """Changes the screen to the game screen"""
        self._screen = Screen.GAME
        self._snake.startTimer()
        self._scoreBoard.reset()

    def _screenToScoreBoard(self) -> None:
        """Changes the screen to the scoreboard screen"""
        self._screen = Screen.SCOREBOARD
    
    def _screenToGameOver(self) -> None:
        """Changes the screen to the game over screen"""
        self._screen = Screen.GAMEOVER
    
    def _saveSnakeDesign(self) -> None:
        """Saves the snake design"""
        self._snake.saveDesign(self._snakeDesign)
        self._screen = Screen.START
    
    def _addToSnakeDesign(self) -> None:
        """Add an element to the snake design"""
        self._snakeDesign.append('#ffffff')
    
    def _removeFromSnakeDesign(self) -> None:
        """Remove the back element from the snake design"""
        self._snakeDesign.pop(-1)

