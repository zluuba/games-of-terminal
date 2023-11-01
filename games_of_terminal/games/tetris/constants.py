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

FLIP_BLOCK = KEY_UP
DOWN = KEY_DOWN

# little square size
CELL_HEIGHT = 1
CELL_WIDTH = 2
