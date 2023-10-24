import curses


DIRECTIONS = {
    curses.KEY_RIGHT: curses.KEY_LEFT,
    curses.KEY_LEFT: curses.KEY_RIGHT,
    curses.KEY_UP: curses.KEY_DOWN,
    curses.KEY_DOWN: curses.KEY_UP,
}

SNAKE_SKIN = 'O'
FOOD_SKIN = '×'
SKINS = ['#', 'O', '×', '¤', '■', '█', '≡', '©']
