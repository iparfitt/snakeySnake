import pygame
import os

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
        self.display = display
        self.score = 0
        self.pastScores = []

    def addAppleCollected(self) -> None:
        """Increase the score by an apple collected"""
        self.score += 250
    
    def addTimeSurvived(self, time) -> None:
        """Increase the score by the time survived"""
        self.score += 5 * time

    def writeToFile(self) -> None:
        """Write the current score to file"""

        with open(os.path.join(absolutePath, "data/scoreboard.txt"), "r") as fRead:
            line = fRead.readline()
            while line != '':
                self.pastScores.append(float(line.split(",")[1].strip()))
                line = fRead.readline()
            self.pastScores.append(round(self.score))
            self.pastScores.sort(reverse = True)
        
        with open(os.path.join(absolutePath, "data/scoreboard.txt"), "w") as fWrite:
            place = 1
            for score in self.pastScores:
                fWrite.write(str(place) + "," + str(round(score)) + "\n")
                place += 1

    def displayCurrentScore(self, 
                            borderWidth: float) -> None:
        """Display the current score on the screen

        Args:
            borderWidth (float): The width of the screen's border
        """
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render(str(int(self.score)), 
                           True, 
                           "white")
        textRect = text.get_rect()
        textRect.top = borderWidth + 10
        textRect.left = borderWidth + 10
        self.display.blit(text, textRect)

    def displayPastScores(self) -> None:
        """Display local score history"""

        font = pygame.font.Font('freesansbold.ttf', 20)

        numScores = 5
        if self.pastScores.__len__() < 5:
            numScores = self.pastScores.__len__()

        for idx in range(0, numScores):
            if (abs(int(self.pastScores[idx]) - self.score) < 2):
                text = font.render(str(idx + 1) + ". " + str(int(self.pastScores[idx])), 
                                   True, 
                                   "green")
            else:
                text = font.render(str(idx + 1) + ". " + str(int(self.pastScores[idx])), 
                                   True, 
                                   "blue")
            textRect = text.get_rect()
            x, y = self.display.get_size()
            textRect.center = x/2, 5 * y/12 + 20*idx
            self.display.blit(text, textRect)