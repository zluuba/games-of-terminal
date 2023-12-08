from curses import KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN


RULES = (
    'Minesweeper is a game where mines are hidden in a grid of squares. '
    'Safe squares have numbers telling you how many mines touch the square. '
    'You can use the number clues to solve the game by opening all of the safe squares. '
    'If you click on a mine you lose the game.'
)

CELL_HEIGHT = 3
CELL_WIDTH = 7

DIRECTIONS = {
    KEY_LEFT: (0, -CELL_WIDTH), KEY_RIGHT: (0, CELL_WIDTH),
    KEY_UP: (-CELL_HEIGHT, 0), KEY_DOWN: (CELL_HEIGHT, 0),
    ord('a'): (0, -CELL_WIDTH), ord('d'): (0, CELL_WIDTH),
    ord('w'): (-CELL_HEIGHT, 0), ord('s'): (CELL_HEIGHT, 0),
}

CELL_OFFSETS = (
    (-CELL_HEIGHT, -CELL_WIDTH), (CELL_HEIGHT, CELL_WIDTH),
    (-CELL_HEIGHT, CELL_WIDTH), (CELL_HEIGHT, -CELL_WIDTH),
    (CELL_HEIGHT, 0), (-CELL_HEIGHT, 0),
    (0, -CELL_WIDTH), (0, CELL_WIDTH),
)
