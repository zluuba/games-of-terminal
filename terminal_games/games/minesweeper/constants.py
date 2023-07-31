import curses


DIRECTIONS = {
    curses.KEY_RIGHT: (0, 1), curses.KEY_LEFT: (0, -1),
    curses.KEY_UP: (-1, 0), curses.KEY_DOWN: (1, 0),
}
FIELD = [[1, 2, 3, 4, 5],
         [6, 7, 8, 9, 10],
         [11, 12, 13, 14, 15],
         [16, 17, 18, 19, 20],
         [21, 22, 23, 24, 25]]
