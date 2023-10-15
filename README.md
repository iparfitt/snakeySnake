# snakeySnake

Version: 0.1.1

## Structure:
    .
    ├── build                   # Compiled files (alternatively `dist`)
    ├── snakeySnake             # Source files
        ├── data                # Data used in the application
            ├── apple.png       # The image used for apples
            ├── scoreboard.txt  # Local record of scores
        ├── __init__.py
        ├── __main__.py         # Main program file
        ├── button.py
        ├── context.py
        ├── controlScreen.py
        ├── enums.py
        ├── game.py
        ├── gameOverScreen.py
        ├── gameScreen.py
        ├── scoreboard.py
        ├── scoreBoardScreen.py
        ├── screen.py
        ├── snake.py
        ├── snakeDesignScreen.py
        ├── startScreen.py
    ├── tests                   # Automated tests
    ├── LICENSE
    └── README.md

## Requirements
python = ">=3.7"
pygame==2.1.3.dev8

## To install
Run `pip3 install snakeySnake` from command line

## To run:
- Run `snakeySnake` from the command line
- Move using "ASWD" or arrow keys
- Collect points by collecting apples and survivng 
- Game over if the snake runs into itself or any walls

## Previous Versions
- v0.0.1: Classic snake game with keyboard controls and local scoreboard
- v0.0.2: Added tutorial and homescreen, pulled enums into separate file
- v0.0.2b: Patch release, fixed bugs with scoreboard not update or writing to file
- v0.1.0: Added capability to design snake and store snake design locally, refactored screens into classes to enable easier future development. Also moved shared object to context object
- v0.1.1: Fixing README