# snakeySnake

Version: 0.0.1

## Structure:
    .
    ├── build                   # Compiled files (alternatively `dist`)
    ├── snakeySnake             # Source files
        ├── data                # Data used in the application
            ├── apple.png       # The image used for apples
            ├── scoreboard.txt  # Local record of scores
        ├── __init__.py
        ├── __main__.py         # Main program file
        ├── game.py
        ├── scoreboard.py
        ├── snake.py
    ├── tests                   # Automated tests
    ├── LICENSE
    └── README.md

## Requirements
python = ">=3.7"
pygame==2.1.3.dev8

## To run:
- Run `snake-cli` from the command line
- Move using "ASWD" or arrow keys
- Collect points by collecting apples and survivng 
- Game over if the snake runs into itself or any walls

## Previous Versions
- v0.0.1: Classic snake game with keyboard controls and local scoreboard