import pygame

# A Class that defines a button that can be pressed in a display
class Button:
    def __init__(self, 
                 display: pygame.Surface,
                 x: float, 
                 y: float,
                 text: str,
                 fontSize: int,
                 onClick) -> None:
        """Initialises a button object

        Args:
            display  (pygame.Surface): The surface to place the button on
            x        (float): The left x value of the button
            y        (float): The top y value of the button
            text     (str): The text to display on the button
            fontSize (int): The font size of the text
            onClick  (function(None)): The function to play when the button is clicked
        """
        self._display = display
        
        font = pygame.font.Font('freesansbold.ttf', fontSize)
        self._text = font.render(text, 
                                True, 
                                "black")
        self._textRect = self._text.get_rect()
        self._textRect.center = (x, y)
        self._buttonSurface = pygame.Surface((len(text) * 0.75 * fontSize, fontSize))
        self._buttonRect = pygame.Rect(0, 0, len(text) * 0.75 * fontSize, fontSize)
        self._buttonRect.center = (x, y)

        self._onClick = onClick

        self._fillColors = {'normal': '#ffffff',
                            'hover': '#666666',
                            'pressed': '#333333'}
    
    def process(self, events: list) -> None:
        """Determine if the button has been pressed, and change the surface accordingly
        Args:
            events (list): A list of pygame events
        """

        if (self._isPressed(events)):
            self._onClick()
        
        self._buttonSurface.blit(self._text, [self._buttonRect.width/2 - self._textRect.width/2,
                                            self._buttonRect.height/2 - self._textRect.height/2])
        self._display.blit(self._buttonSurface, self._buttonRect)
    
    def _isPressed(self, events: list) -> bool:
        """Return true if the button has been pressed, false otherwise
        Args:
            events (list): A list of pygame events
        """

        mousePos = pygame.mouse.get_pos()
        self._buttonSurface.fill(self._fillColors['normal'])
        if (self._buttonRect.collidepoint(mousePos)):
            self._buttonSurface.fill(self._fillColors['hover'])

            for event in events:
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    self._buttonSurface.fill(self._fillColors['pressed'])
                    return True
        return False