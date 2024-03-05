# Upcoming Features
Here are some features I'm planning to implement in future releases.


## Upcoming Games:
- Connect 4
- 2048 Game
- Sea Battle
- Sudoku
- Wordle

## Upcoming Features:
- Confess All in Settings
- Custom color schemes
- Progress saving and 'do you want to continue prev game?' for unfinished games
- Ability to hide side menu
- Easter egg in Main Menu ("Burnout Mode" - hide the menu, leaving only the fire)
- Main Menu rebuilding
- Ability to add own game control keys
- Sounds

- Tetris features:
    - feature: add game field size handle (keep the same proportion)
    - feature: add a slight delay after line removal (and highlight the line)
    - feature: add +5,000 points if the user clears the board and the score > 0

## Refactoring & Bug Fixing
- bug: time spent in pause is counted in the statistics

- Tetris game:
    - bug: blocks move after pause without keeping interval

- Snake game:
    - bug: obstacles can appear in front of the snake and cause an undeserved loss
    - bug: snake vertical speed should be half the horizontal speed, but it is currently equal
