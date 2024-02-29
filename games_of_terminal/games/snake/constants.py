from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN


GAME_TIPS = {
    'Move': '← ↓ ↑ →',
    'Pause': 'P',
}

DIRECTIONS = {
    KEY_RIGHT: KEY_LEFT,
    KEY_LEFT: KEY_RIGHT,
    KEY_UP: KEY_DOWN,
    KEY_DOWN: KEY_UP,
}

# 'ᕱ' '⌂', '⎍'
OBSTACLES_SKINS = ['۩', 'ᚾ', 'ᛅ', '⏏', '⋂']

COLORS = {
    'Boring': {
        'snake': 'bright_white_text_black_bg',
        'food': 'very_bright_dull_pastel_yellow_green_text_black_bg',
        'obstacles': 'strong_pastel_blue_text_black_bg',
    },
    'Snow': {
        'snake': 'white_text_black_color',
        'food': 'bright_white_text_black_bg',
        'obstacles': 'dark_medium_blue_text_black_bg',
    },
    'Desert': {
        'snake': 'pastel_light_peach_text_black_bg',
        'food': 'very_bright_yellow_text_black_bg',
        'obstacles': 'pastel_brown_red_text_black_bg',
    },
}
