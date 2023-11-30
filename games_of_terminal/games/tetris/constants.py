"""
Blocks:

I-block
    initial:  '#'
              '#'
              '#'
              '#'

    flipped:  '# # # #'

J-block
    initial:   '#'
               '#'
             '# #'

    flipped:  '#'        '# #'    '# # #'
              '# # #'      '#'        '#'
                           '#'

L-block
    initial:  '#'
              '#'
              '# #'

    flipped:  '# # #'    '# #'        '#'
              '#'        '#'      '# # #'
                         '#'

O-block
    initial:  '# #'
              '# #'

Z-block
    initial:  '# #'
                '# #'

    flipped:    '#'
              '# #'
              '#'

T-block
    initial:  '# # #'
                '#'

    flipped:    '#'      '#'      '#'
              '# #'    '# # #'    '# #'
                '#'               '#'

S-block
    initial:    '# #'
              '# #'

    flipped:  '#'
              '# #'
                '#'

"""

from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN


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

# little square size
CELL_HEIGHT = 1
CELL_WIDTH = 2

BLOCK_COLORS = {
    'free': 'white_text_light_black_bg',
    'placed_block': 'black_text_pastel_dirty_blue_bg',
    'I-block': 'white_text_pastel_blue_bg',
    'J-block': 'white_text_green_bg',
    'L-block': 'white_text_deep_blue_bg',
    'O-block': 'white_text_pink_bg',
    'Z-block': 'white_text_yellow_bg',
    'T-block': 'black_text_deep_pink_bg',
    'S-block': 'white_text_light_purple_bg',
}
