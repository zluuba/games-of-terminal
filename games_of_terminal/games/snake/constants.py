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
OBSTACLES_COLOR = 'purple_text_black_bg'
