from games_of_terminal.constants import KEYS


CELL_HEIGHT = 3
CELL_WIDTH = 7

CELL_OFFSETS = (
    (-CELL_HEIGHT, -CELL_WIDTH), (CELL_HEIGHT, CELL_WIDTH),
    (-CELL_HEIGHT, CELL_WIDTH), (CELL_HEIGHT, -CELL_WIDTH),
    (CELL_HEIGHT, 0), (-CELL_HEIGHT, 0),
    (0, -CELL_WIDTH), (0, CELL_WIDTH),
)

DIRECTIONS = {
    KEYS['left_arrow']: (0, -CELL_WIDTH), KEYS['right_arrow']: (0, CELL_WIDTH),
    KEYS['up_arrow']: (-CELL_HEIGHT, 0), KEYS['down_arrow']: (CELL_HEIGHT, 0),
    ord('a'): (0, -CELL_WIDTH), ord('d'): (0, CELL_WIDTH),
    ord('w'): (-CELL_HEIGHT, 0), ord('s'): (CELL_HEIGHT, 0),
}

GAME_TIPS = {
    'Move': '← ↓ ↑ → (wasd)',
    'Open cell': 'Enter',
    'Place flag': 'Q',
}

COLORS = {
    'Blue Jeans': {
        0: 'white_text_pastel_blue_bg',
        1: 'white_text_light_blue_bg',
        2: 'white_text_medium_blue_bg',
        3: 'white_text_dark_medium_blue_bg',
        4: 'white_text_deep_blue_bg',
        'bomb': 'white_text_red_bg',
        'closed': 'white_text_black_bg',
        'cursor': 'white_text_light_grey_bg',
        'flag': 'white_text_deep_purple_bg',
    },
    'Sweet Summer Child': {
        0: 'black_text_light_pastel_lettuce_bg',
        1: 'black_text_light_lettuce_bg',
        2: 'black_text_pastel_light_peach_bg',
        3: 'black_text_light_pastel_purple_bg',
        4: 'black_text_dark_orange_bg',
        'bomb': 'black_text_peaceful_strong_purple_bg',
        'closed': 'white_text_black_bg',
        'cursor': 'black_text_very_light_grey_brighter_v1_bg',
        'flag': 'black_text_peach_bg',
    },
    'Dragon Burn': {
        0: 'white_text_light_grey_brighter_v2_bg',
        1: 'white_text_light_grey_bg',
        2: 'white_text_grey_brighter_v1_bg',
        3: 'white_text_medium_grey_brighter_v1_bg',
        4: 'white_text_dark_grey_bg',
        'bomb': 'black_text_grey_white_brighter_v3_bg',
        'closed': 'white_text_black_bg',
        'cursor': 'white_text_dark_grey_brighter_v2_bg',
        'flag': 'black_text_very_light_grey_brighter_v1_bg',
    },
}
