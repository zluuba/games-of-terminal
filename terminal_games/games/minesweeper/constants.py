import curses


RULES = (
    'Minesweeper is a game where mines are hidden in a grid of squares. '
    'Safe squares have numbers telling you how many mines touch the square. '
    'You can use the number clues to solve the game by opening all of the safe squares. '
    'If you click on a mine you lose the game.'
)

CELL_HEIGHT = 3
CELL_WIDTH = 7

# offset to ensure that game cells do not touch the edge
# of the game field (-1 on each side)
GAME_FIELD_OFFSET_XY = 2

DIRECTIONS = {
    curses.KEY_LEFT: (0, -CELL_WIDTH), curses.KEY_RIGHT: (0, CELL_WIDTH),
    curses.KEY_UP: (-CELL_HEIGHT, 0), curses.KEY_DOWN: (CELL_HEIGHT, 0),
    ord('a'): (0, -CELL_WIDTH), ord('d'): (0, CELL_WIDTH),
    ord('w'): (-CELL_HEIGHT, 0), ord('s'): (CELL_HEIGHT, 0),
}

CELL_OFFSETS = (
    (-CELL_HEIGHT, -CELL_WIDTH), (CELL_HEIGHT, CELL_WIDTH),
    (-CELL_HEIGHT, CELL_WIDTH), (CELL_HEIGHT, -CELL_WIDTH),
    (CELL_HEIGHT, 0), (-CELL_HEIGHT, 0),
    (0, -CELL_WIDTH), (0, CELL_WIDTH),
)
