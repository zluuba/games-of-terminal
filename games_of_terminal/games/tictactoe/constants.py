from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN


CELLS_IN_ROW = 3

DIRECTIONS = {
    KEY_RIGHT: (0, 1), KEY_LEFT: (0, -1),
    KEY_UP: (-1, 0), KEY_DOWN: (1, 0),
}

WINNING_PATTERNS = (
    (1, 2, 3), (4, 5, 6), (7, 8, 9),
    (1, 4, 7), (2, 5, 8), (3, 6, 9),
    (1, 5, 9), (3, 5, 7),
)

BEST_MOVE_PATTERNS_BY_OWNERS = (
    ('computer', 'computer', 'free'),
    ('user', 'user', 'free'),
)

GAME_TIPS = {
    'Move': '← ↓ ↑ →',
    'Select cell': 'Enter',
}
