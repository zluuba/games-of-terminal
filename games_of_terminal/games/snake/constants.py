from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN


DIRECTIONS = {
    KEY_RIGHT: KEY_LEFT,
    KEY_LEFT: KEY_RIGHT,
    KEY_UP: KEY_DOWN,
    KEY_DOWN: KEY_UP,
}

SNAKE_SKIN = 'O'
FOOD_SKIN = '×'
SKINS = ['#', 'O', '×', '¤', '■', '█', '≡', '©']
