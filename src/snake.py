import pygame

class Snake():
    def __init__(self):
        print("Initialising snake")
        self.blue = (0,0,255)
        self.red = (255,0,0)
    
    def drawPixel(self, display):
        pygame.draw.rect(display, self.blue,[200,150,10,10])