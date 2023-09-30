import pygame

from snakeySnake.context import Context
from snakeySnake.controlScreen import ControlScreen
from snakeySnake.enums import ScreenEnum
from snakeySnake.gameOverScreen import GameOverScreen
from snakeySnake.gameScreen import GameScreen
from snakeySnake.snakeDesignScreen import SnakeDesignScreen
from snakeySnake.scoreBoardScreen import ScoreBoardScreen
from snakeySnake.startScreen import StartScreen

# The main class describing a snake game
class Game:
    def __init__(self) -> None:
        """Initialises a game object"""
        self._context = Context()

        self._displayScreen = {ScreenEnum.CONTROLS: ControlScreen(self._context),
                               ScreenEnum.GAMEOVER: GameOverScreen(self._context),
                               ScreenEnum.GAME: GameScreen(self._context),
                               ScreenEnum.SCOREBOARD: ScoreBoardScreen(self._context),
                               ScreenEnum.SNAKEDESIGN: SnakeDesignScreen(self._context),
                               ScreenEnum.START: StartScreen(self._context)}

        self._gameOver = False
        self._exit = False

    def run(self) -> None:
        """Run the main loop of the game"""

        while (not self._exit):
            events = pygame.event.get()
            for event in events:
                # Quit game
                if (event.type == pygame.QUIT):
                    self._exit = True

            self._displayScreen[self._context.getCurrentScreen()].draw(events)
            pygame.display.flip()
            self._context.updateTimer()
        
        pygame.quit()
        quit()
