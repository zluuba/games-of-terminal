from games_of_terminal.constants import KEYS


# standard Tetris field size: 20 x 10
FIELD_HEIGHT = 20
FIELD_WIDTH = 10

# little square size
CELL_WIDTH = 2
CELL_HEIGHT = 1

FALLING_DIRECTION = 'down'
DIRECTIONS = {
    KEYS['left_arrow']: 'left',
    KEYS['right_arrow']: 'right',
    KEYS['down_arrow']: 'down',
}

OFFSETS = {
    'left': (0, -1),
    'right': (0, 1),
    'down': (1, 0),
}

FLIP_BLOCK = KEYS['up_arrow']
DROP_BLOCK = ord(' ')
DOWN = KEYS['down_arrow']

# max height of blocks (4 - I-block) + borders (2)
NEXT_BLOCK_AREA_HEIGHT = 6
NEXT_BLOCK_TEXT = 'next block'

# rows: points you get if remove this num of rows in one move
SCORES = {
    0: 0,
    1: 100,
    2: 300,
    3: 1_000,
    4: 2_400,
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

GAME_TIPS = {
    'Move': '← ↓ →',
    'Flip': '↑',
    'Drop': 'Space',
    'Pause': 'P',
}

COLORS = {
    'Dispersion': {
        'free': 'white_text_light_black_bg',
        'I-block': 'white_text_pastel_deep_blue_bg',
        'J-block': 'white_text_medium_blue_bg',
        'L-block': 'white_text_bright_light_orange_bg',
        'O-block': 'white_text_pastel_yellow_bg',
        'Z-block': 'white_text_peaceful_red_bg',
        'T-block': 'white_text_strong_magenta_bg',
        'S-block': 'white_text_green_bg',
    },
    '90\'s': {
        'free': 'white_text_light_black_bg',
        'I-block': 'black_text_light_pastel_lettuce_bg',
        'J-block': 'white_text_pastel_blue_bg',
        'L-block': 'black_text_very_bright_pastel_light_yellow_v2_bg',
        'O-block': 'white_text_bright_light_pastel_orange_bg',
        'Z-block': 'black_text_very_bright_light_pastel_pink_bg',
        'T-block': 'black_text_pastel_light_peach_bg',
        'S-block': 'black_text_light_pastel_purple_bg',
    },
    '50 Shades of Gray': {
        'free': 'white_text_light_black_bg',
        'I-block': 'white_text_light_grey_bg',
        'J-block': 'black_text_very_light_grey_brighter_v1_bg',
        'L-block': 'black_text_grey_white_brighter_v3_bg',
        'O-block': 'black_text_white_bg',
        'Z-block': 'white_text_grey_brighter_v1_bg',
        'T-block': 'white_text_light_grey_brighter_v2_bg',
        'S-block': 'white_text_medium_grey_bg',
    },
}
