from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN


# standard Tetris field size: 10 (width) x 20 (height)
FIELD_WIDTH = 10

# little square size
CELL_WIDTH = 2
CELL_HEIGHT = 1

# 1 on each side
BASE_OFFSET = 2


BLOCKS = {
    'I-block': [
        [1], [1], [1], [1],
    ],
    'J-block': [
        [0, 1],
        [0, 1],
        [1, 1],
    ],
    'L-block': [
        [1, 0],
        [1, 0],
        [1, 1],
    ],
    'O-block': [
        [1, 1],
        [1, 1],
    ],
    'Z-block': [
        [1, 1, 0],
        [0, 1, 1],
    ],
    'T-block': [
        [1, 1, 1],
        [0, 1, 0],
    ],
    'S-block': [
        [0, 1, 1],
        [1, 1, 0],
    ],
}

DIRECTIONS = {
    KEY_LEFT: 'left',
    KEY_RIGHT: 'right',
    KEY_DOWN: 'down',
}

OFFSETS = {
    'left': (0, -1),
    'right': (0, 1),
    'down': (1, 0),
}

FLIP_BLOCK = KEY_UP
DROP_BLOCK = ord(' ')
DOWN = KEY_DOWN

BLOCK_COLORS = {
    'free': 'white_text_light_black_bg',
    'placed_block': 'white_text_deep_purple_bg',
    'I-block': 'white_text_pastel_blue_bg',
    'J-block': 'white_text_green_bg',
    'L-block': 'white_text_deep_blue_bg',
    'O-block': 'white_text_pink_bg',
    'Z-block': 'white_text_yellow_bg',
    'T-block': 'black_text_deep_pink_bg',
    'S-block': 'white_text_light_purple_bg',
}

# all scores multiplying by current level
SCORES = {
    'single': 100,          # 1 row
    'double': 300,          # 2 rows
    'triple': 1000,         # 3 rows
    'full rows': 2400,      # 4 rows
    'combo': 100,           # remove lines 2+ times straight
}
