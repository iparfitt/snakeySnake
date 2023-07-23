from snake import Snake
from scoreboard import ScoreBoard

import pygame

class Game:
    def __init__(self):
        print("Initialising game")
        self.snake = Snake()
        self.scoreBoard = ScoreBoard()

    def run(self):
        # Initialise board
        pygame.init()
        display = pygame.display.set_mode((400,300))
        pygame.display.update()
        pygame.display.set_caption('Snake Game')

        game_over = False
        while not game_over:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    game_over=True
            
            self.snake.drawPixel(display)
            pygame.display.update()

        pygame.quit()
        quit()
    