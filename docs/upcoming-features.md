# Upcoming Features
Here are some features I plan to implement in future releases, along with a list of bugs to fix.


## Upcoming Games:
- Connect 4
- 2048 Game
- Sea Battle
- Sudoku
- Wordle
- Crossy Road
- Doom

## Upcoming Features:
- Main Menu rebuilding: add pagination for games
- Logger rebuilding & adding it to the GOT
- Easter egg in Main Menu ("Burnout Mode" - hide the menu, leaving only the fire)
- Switch DB logic from raw SQL to SQLAlchemy
- Confess All in Settings
- Custom color schemes
- Progress saving and 'do you want to continue prev game?' for unfinished games
- Ability to hide side menu
- Ability to add own game control keys
- Sounds
- More tests

- Tetris features:
    - feature: add game field size handle (keep the same proportion)
    - feature: add a slight delay after line removal (and highlight the line)
    - feature: add +5,000 points if the user clears the board and the score > 0

## Bugs
- time spent in pause is counted in the statistics
- blocks move after pause without keeping interval (Tetris game)
- obstacles can appear in front of the snake and cause an undeserved loss (Snake game)
- snake vertical speed should be half the horizontal speed, but it is currently equal (Snake game)
- 'check' function in main Achievement Manager - unnecessary **kwargs arguments, get rid of it.
