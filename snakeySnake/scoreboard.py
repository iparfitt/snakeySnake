import pygame
import os
import math

absolutePath = os.path.dirname(__file__)

# A class which described the score history of the game
class ScoreBoard:
    # Score:
    # + 250 points for every apple collected
    # + 5 points for every second survived
    def __init__(self, 
                 display: pygame.display) -> None:
        """Initialises a ScoreBoard

        Args:
            display (pygame.display): The surface to place the score board on
        """
        self._display = display
        self._score = 0
        self._pastScores = []

        # Populate past scores if data is available
        if os.path.isfile(os.path.join(absolutePath, "data/scoreboard.txt")):
            with open(os.path.join(absolutePath, "data/scoreboard.txt"), "r") as fRead:
                line = fRead.readline()
                while line != '':
                    self._pastScores.append(float(line.split(",")[1].strip()))
                    line = fRead.readline()

    def addAppleCollected(self) -> None:
        """Increase the score by an apple collected"""
        self._score += 250
    
    def addTimeSurvived(self, time) -> None:
        """Increase the score by the time survived"""
        self._score += 5 * time

    def writeToFile(self) -> None:
        """Write the current score to file"""
        self._pastScores.append(math.floor(self._score))
        self._pastScores.sort(reverse = True)
        
        with open(os.path.join(absolutePath, "data/scoreboard.txt"), "w") as fWrite:
            place = 1
            for score in self._pastScores:
                fWrite.write(str(place) + "," + str(math.floor(score)) + "\n")
                place += 1

    def displayCurrentScore(self, 
                            borderWidth: float) -> None:
        """Display the current score on the screen

        Args:
            borderWidth (float): The width of the screen's border
        """
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render(str(int(self._score)), 
                           True, 
                           "white")
        textRect = text.get_rect()
        textRect.top = borderWidth + 10
        textRect.left = borderWidth + 10
        self._display.blit(text, textRect)

    def displayPastScores(self) -> None:
        """Display local score history"""

        font = pygame.font.Font('freesansbold.ttf', 20)

        numScores = 5
        if self._pastScores.__len__() < 5:
            numScores = self._pastScores.__len__()

        for idx in range(numScores):
            if (self._pastScores[idx] == math.floor(self._score)):
                text = font.render(str(idx + 1) + ". " + str(int(self._pastScores[idx])), 
                                   True, 
                                   "green")
            else:
                text = font.render(str(idx + 1) + ". " + str(int(self._pastScores[idx])), 
                                   True, 
                                   "blue")
            textRect = text.get_rect()
            x, y = self._display.get_size()
            textRect.center = x/2, 5 * y/12 + 20*idx
            self._display.blit(text, textRect)
    
    def reset(self) -> None:
        """Resets the scoreboard"""
        self._score = 0