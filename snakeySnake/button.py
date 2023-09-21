import pygame

# A Class that defines a button that can be pressed in a display
class Button:
    def __init__(self, 
                 display: pygame.display, 
                 x: float, 
                 y: float,
                 text: str, 
                 onClick) -> None:
        """Initialises a button object

        Args:
            display (pygame.display): The surface to place the button on
            x       (float): The left x value of the button
            y       (float): The top y value of the button
            text    (str): The text to display on the button
            onClick (function(None)): The function to play when the button is clicked
        """
        self.display = display
        
        font = pygame.font.Font('freesansbold.ttf', 20)
        self.text = font.render(text, 
                                True, 
                                "black")
        self.textRect = self.text.get_rect()
        self.textRect.center = [x, y]
        self.buttonSurface = pygame.Surface((len(text) * 15, 20))
        self.buttonRect = pygame.Rect(0, 0, len(text) * 15, 20)
        self.buttonRect.center = [x, y]

        self.onClick = onClick

        self.fillColors = {'normal': '#ffffff',
                           'hover': '#666666',
                           'pressed': '#333333'}
    
    def process(self) -> None:
        """Determine if the button has been pressed, and change the surface accordingly"""

        if (self._isPressed()):
            self.onClick()
        
        self.buttonSurface.blit(self.text, [self.buttonRect.width/2 - self.textRect.width/2,
                                            self.buttonRect.height/2 - self.textRect.height/2])
        self.display.blit(self.buttonSurface, self.buttonRect)
    
    def _isPressed(self) -> None:
        """Return true if the button has been pressed, false otherwise"""

        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if (self.buttonRect.collidepoint(mousePos)):
            self.buttonSurface.fill(self.fillColors['hover'])

            for event in pygame.event.get():
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    self.buttonSurface.fill(self.fillColors['pressed'])
                    return True
        return False