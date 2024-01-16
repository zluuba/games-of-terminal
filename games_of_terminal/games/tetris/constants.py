from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN


# standard Tetris field size: 20 x 10
FIELD_HEIGHT = 20
FIELD_WIDTH = 10

# little square size
CELL_WIDTH = 2
CELL_HEIGHT = 1

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

FALLING_DIRECTION = 'down'

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
    'I-block': 'white_text_pastel_deep_blue_bg',
    'J-block': 'white_text_medium_blue_bg',
    'L-block': 'white_text_bright_light_orange_bg',
    'O-block': 'white_text_pastel_yellow_bg',
    'Z-block': 'white_text_peaceful_red_bg',
    'T-block': 'white_text_strong_magenta_bg',
    'S-block': 'white_text_green_bg',
}

# max height of blocks (4 - I-block) + borders (2)
NEXT_BLOCK_AREA_HEIGHT = 6
NEXT_BLOCK_TEXT = 'next block'

# rows: points you get if remove this num of rows in one move
SCORES = {
    0: 0,
    1: 100,          # 1 row, 'single'
    2: 300,          # 2 rows, 'double'
    3: 1_000,         # 3 rows, 'triple'
    4: 2_400,         # 4 rows, 'four!'
    # 'combo': 100,    # remove lines 2+ times straight
}

# level: points you need to gain to move up this level
LEVELS = {
    1: 0,
    2: 2_000,
    3: 5_000,
    4: 10_000,
    5: 20_000,
}

LEVEL_SPEED_DIFF = 0.2

GAME_TIPS = {
    'Move': '← ↓ →',
    'Flip': '↑',
    'Drop': 'Space',
    'Pause': 'P',
}
