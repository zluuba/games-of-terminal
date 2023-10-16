import curses


DIRECTIONS = {
    curses.KEY_RIGHT: (0, 1), curses.KEY_LEFT: (0, -1),
    curses.KEY_UP: (-1, 0), curses.KEY_DOWN: (1, 0),
}
FIELD = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]

WINNING_COMBINATIONS = ((1, 2, 3), (4, 5, 6), (7, 8, 9),
                        (1, 4, 7), (2, 5, 8), (3, 6, 9),
                        (1, 5, 9), (3, 5, 7))

GAME_STATUSES = {
    0: 'User win!',
    1: 'Computer win!',
    2: 'Tie!',
}
