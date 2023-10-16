import curses


RULES = (
    'Minesweeper is a game where mines are hidden in a grid of squares. '
    'Safe squares have numbers telling you how many mines touch the square. '
    'You can use the number clues to solve the game by opening all of the safe squares. '
    'If you click on a mine you lose the game.'
)

SIDE_MENU_TIPS = [
    'Rules     - r',
    'Move      - ← ↓ ↑ →',
    'Quit      - q',
    'Pause     - p',
    'Hide tips - h',
]

DIRECTIONS = {
    curses.KEY_RIGHT: (0, 1), curses.KEY_LEFT: (0, -1),
    curses.KEY_UP: (-1, 0), curses.KEY_DOWN: (1, 0),
}