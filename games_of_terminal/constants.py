from curses import (
    KEY_ENTER, KEY_UP, KEY_DOWN,
    KEY_LEFT, KEY_RIGHT, KEY_RESIZE,
)


APP_NAME = 'Games Of Terminal'

LOGO = [
    ' ####     ####   ######',
    '##       ##  ##    ##  ',
    '##  ###  ##  ##    ##  ',
    '##   ##  ##  ##    ##  ',
    ' #####    ####     ##  ',
]

DEFAULT_Y_OFFSET = 1
DEFAULT_OFFSET = 2
STATUS_BOX_SIZE = 3

MESSAGES = {
    'game_over': 'GAME OVER',
    'score_text': 'Score: ',
    'best_score': 'Best score: ',
    'new_best_score': 'New best score!',
    'start_text': 'Press any key to start',
    'play_again': 'Press Space to play again',
}

KEYS = {
    'space': ord(' '),
    'escape': 27,
    'enter': [KEY_ENTER, 10, 13],
    'up_arrow': KEY_UP,
    'down_arrow': KEY_DOWN,
    'left_arrow': KEY_LEFT,
    'right_arrow': KEY_RIGHT,
    'q': ord('q'),
    'pause': ord('p'),
    'resize': KEY_RESIZE,
    'w': ord('w'),
    's': ord('s'),
    'a': ord('a'),
    'd': ord('d'),
}

GAME_STATUSES = {
    'game_is_on': {'text': 'ON GAME', 'color': 'white_text_dark_grey_bg'},
    'user_win': {'text': 'You WIN!', 'color': 'white_text_green_bg'},
    'user_lose': {'text': 'You LOSE', 'color': 'white_text_red_bg'},
    'tie': {'text': 'TIE', 'color': 'white_text_yellow_bg'},
}

SIDE_MENU_TIPS = {
    'Move': '← ↓ ↑ → (wasd)',
    'Restart': 'r',
    'Tips/rules': 't',
    'Quit': 'esc',
}
