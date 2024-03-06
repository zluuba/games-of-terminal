from games_of_terminal.constants import KEYS


CELLS_IN_ROW = 3
CELL_RATIO_COEFF = 2.5

DIRECTIONS = {
    KEYS['up_arrow']: (-1, 0), KEYS['w']: (-1, 0),
    KEYS['left_arrow']: (0, -1), KEYS['a']: (0, -1),
    KEYS['down_arrow']: (1, 0), KEYS['s']: (1, 0),
    KEYS['right_arrow']: (0, 1), KEYS['d']: (0, 1),
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
    'Move': '← ↓ ↑ → (wasd)',
    'Select cell': 'Enter',
}

COLORS = {
    'Banana Split': {
        'free': 'white_text_dark_grey_bg',
        'cursor': 'white_text_light_grey_bg',
        'user': 'black_text_very_bright_light_pastel_pink_bg',
        'computer': 'black_text_very_bright_pastel_light_yellow_v2_bg',
    },
    'Blues': {
        'free': 'white_text_dark_grey_bg',
        'cursor': 'white_text_light_grey_bg',
        'user': 'black_text_aqua_light_blue_bg',
        'computer': 'black_text_medium_aqua_light_blue_bg',
    },
    'Joker': {
        'free': 'white_text_dark_grey_bg',
        'cursor': 'white_text_light_grey_bg',
        'user': 'black_text_deep_green_bg',
        'computer': 'white_text_deep_purple_bg',
    },
}
