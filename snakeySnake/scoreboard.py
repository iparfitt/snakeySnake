import math
import os
import pygame

absolute_path = os.path.dirname(__file__)


class ScoreBoard:
    """A class which describes the score history of the game"""

    # Score:
    # + 250 points for every apple collected
    # + 5 points for every second survived
    def __init__(self, display: pygame.Surface) -> None:
        """Initialises a ScoreBoard

        Args:
            display (pygame.Surface): The surface to place the score board on
        """
        self._display = display
        self._score = 0
        self._past_scores = []

        # Populate past scores if data is available
        if os.path.isfile(os.path.join(absolute_path, "data/scoreboard.txt")):
            with open(
                os.path.join(absolute_path, "data/scoreboard.txt"),
                "r",
                encoding="UTF-8",
            ) as read:
                line = read.readline()
                while line != "":
                    self._past_scores.append(float(line.split(",")[1].strip()))
                    line = read.readline()

    def add_apple_collected(self) -> None:
        """Increase the score by an apple collected"""
        self._score += 250

    def add_time_survived(self, time) -> None:
        """Increase the score by the time survived"""
        self._score += 5 * time

    def write_to_file(self) -> None:
        """Write the current score to file"""
        self._past_scores.append(math.floor(self._score))
        self._past_scores.sort(reverse=True)

        with open(
            os.path.join(absolute_path, "data/scoreboard.txt"), "w", encoding="UTF-8"
        ) as write:
            place = 1
            for score in self._past_scores:
                write.write(str(place) + "," + str(math.floor(score)) + "\n")
                place += 1

    def display_current_score(self, border_width: int) -> None:
        """Display the current score on the screen

        Args:
            border_width (int): The width of the screen's border
        """
        font = pygame.font.Font("freesansbold.ttf", 20)
        text = font.render(str(int(self._score)), True, "white")
        text_rect = text.get_rect()
        text_rect.top = border_width + 10
        text_rect.left = border_width + 10
        self._display.blit(text, text_rect)

    def display_past_scores(self) -> None:
        """Display local score history"""

        font = pygame.font.Font("freesansbold.ttf", 20)

        num_scores = 5
        if len(self._past_scores) < 5:
            num_scores = len(self._past_scores)

        for idx in range(num_scores):
            if self._past_scores[idx] == math.floor(self._score):
                text = font.render(
                    str(idx + 1) + ". " + str(int(self._past_scores[idx])),
                    True,
                    "green",
                )
            else:
                text = font.render(
                    str(idx + 1) + ". " + str(int(self._past_scores[idx])), True, "blue"
                )
            text_rect = text.get_rect()
            x, y = self._display.get_size()
            text_rect.center = (int(x / 2), int(5 * y / 12 + 20 * idx))
            self._display.blit(text, text_rect)

    def reset(self) -> None:
        """Resets the scoreboard"""
        self._score = 0
