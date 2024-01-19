from curses import (
    KEY_ENTER, KEY_UP, KEY_DOWN,
    KEY_LEFT, KEY_RIGHT, KEY_RESIZE,
    COLOR_WHITE, COLOR_BLACK, COLOR_GREEN,
    COLOR_RED, COLOR_YELLOW,
)


APP_NAME = 'Games Of Terminal'

LOGO = [
    ' ####     ####   ######',
    '##       ##  ##    ##  ',
    '##  ###  ##  ##    ##  ',
    '##   ##  ##  ##    ##  ',
    ' #####    ####     ##  ',
]

MIN_WIN_HEIGHT = 25
MIN_WIN_WIDTH = 80

# 1 on each side
BASE_OFFSET = 2
DEFAULT_YX_OFFSET = 1
STATUS_BOX_HEIGHT = 3

KEYS = {
    'up_arrow': KEY_UP,
    'down_arrow': KEY_DOWN,
    'left_arrow': KEY_LEFT,
    'right_arrow': KEY_RIGHT,
    'enter': [KEY_ENTER, 10, 13],
    'resize': KEY_RESIZE,
    'restart': ord('r'),
    'pause': ord('p'),
    'space': ord(' '),
    'escape': 27,
    'w': ord('w'),
    's': ord('s'),
    'a': ord('a'),
    'd': ord('d'),
    'q': ord('q'),
}

GAMES = [
    'Snake',
    'Minesweeper',
    'Tic Tac Toe',
    'Tetris',
]

GAME_STATUSES = {
    'game_active': {'text': 'ON GAME', 'color': 'white_text_dark_grey_bg'},
    'user_win': {'text': 'You WIN!', 'color': 'white_text_green_bg'},
    'user_lose': {'text': 'You LOSE', 'color': 'white_text_red_bg'},
    'tie': {'text': 'TIE', 'color': 'white_text_yellow_bg'},
}

MESSAGES = {
    'game_over': 'GAME OVER',
    'score_text': 'Score: ',
    'best_score': 'Best score: ',
    'new_best_score': 'New best score!',
    'play_again': 'Press Space to play again',
    'win_resize_menu': 'Resizing..',
    'win_resize_game': [
        'Resizing..',
        'Current game will be RESTARTED.',
    ],
}

COMMON_TIPS = {
    'Restart': 'R',
    'Settings': 'S',
    'Quit': 'Esc',
}

# based on curses initial color pair (0: white text, black bg)
DEFAULT_COLOR = 0

COLOR_MAPPING = {
    'white_text_green_bg': {
        'pair_num': 1,
        'text_color': COLOR_WHITE,
        'bg_color': COLOR_GREEN,
    },
    'white_text_red_bg': {
        'pair_num': 2,
        'text_color': COLOR_WHITE,
        'bg_color': COLOR_RED,
    },
    'white_text_dark_grey_bg': {
        'pair_num': 3,
        'text_color': COLOR_WHITE,
        'bg_color': 236,
    },
    'white_text_light_grey_bg': {
        'pair_num': 4,
        'text_color': COLOR_WHITE,
        'bg_color': 245,
    },
    'white_text_pink_bg': {
        'pair_num': 5,
        'text_color': COLOR_WHITE,
        'bg_color': 132,
    },
    'white_text_light_purple_bg': {
        'pair_num': 6,
        'text_color': COLOR_WHITE,
        'bg_color': 134,
    },
    'red_text_black_bg': {
        'pair_num': 7,
        'text_color': COLOR_RED,
        'bg_color': COLOR_BLACK,
    },
    'green_text_black_bg': {
        'pair_num': 8,
        'text_color': COLOR_GREEN,
        'bg_color': COLOR_BLACK,
    },
    'yellow_text_black_bg': {
        'pair_num': 9,
        'text_color': COLOR_YELLOW,
        'bg_color': COLOR_BLACK,
    },
    'black_text_red_bg': {
        'pair_num': 10,
        'text_color': COLOR_BLACK,
        'bg_color': COLOR_RED,
    },
    'black_text_deep_pink_bg': {
        'pair_num': 11,
        'text_color': COLOR_BLACK,
        'bg_color': 168,
    },
    'black_text_pastel_dirty_blue_bg': {
        'pair_num': 12,
        'text_color': COLOR_BLACK,
        'bg_color': 153,
    },
    'white_text_pastel_blue_bg': {
        'pair_num': 13,
        'text_color': COLOR_WHITE,
        'bg_color': 111,
    },
    'white_text_light_blue_bg': {
        'pair_num': 14,
        'text_color': COLOR_WHITE,
        'bg_color': 75,
    },
    'white_text_medium_blue_bg': {
        'pair_num': 15,
        'text_color': COLOR_WHITE,
        'bg_color': 68,
    },
    'white_text_dark_medium_blue_bg': {
        'pair_num': 16,
        'text_color': COLOR_WHITE,
        'bg_color': 26,
    },
    'white_text_deep_blue_bg': {
        'pair_num': 17,
        'text_color': COLOR_WHITE,
        'bg_color': 17,
    },
    'white_text_deep_purple_bg': {
        'pair_num': 18,
        'text_color': COLOR_WHITE,
        'bg_color': 54,
    },
    'white_text_yellow_bg': {
        'pair_num': 19,
        'text_color': COLOR_WHITE,
        'bg_color': 136,
    },
    'strong_pastel_purple_text_black_bg': {
        'pair_num': 20,
        'text_color': 147,
        'bg_color': COLOR_BLACK,
    },
    'light_grey_text_black_bg': {
        'pair_num': 21,
        'text_color': 245,
        'bg_color': COLOR_BLACK,
    },
    'white_text_light_black_bg': {
        'pair_num': 22,
        'text_color': COLOR_WHITE,
        'bg_color': 232,
    },
    'light_black_text_black_bg': {
        'pair_num': 23,
        'text_color': 233,
        'bg_color': COLOR_BLACK,
    },
    'very_light_grey_text_black_bg': {
        'pair_num': 24,
        'text_color': 248,
        'bg_color': COLOR_BLACK,
    },
    'grey_text_black_bg': {
        'pair_num': 25,
        'text_color': 242,
        'bg_color': COLOR_BLACK,
    },
    'white_text_bright_light_orange_bg': {
        'pair_num': 26,
        'text_color': COLOR_WHITE,
        'bg_color': 208,
    },
    'white_text_peaceful_red_bg': {
        'pair_num': 27,
        'text_color': COLOR_WHITE,
        'bg_color': 124,
    },
    'white_text_pastel_yellow_bg': {
        'pair_num': 28,
        'text_color': COLOR_WHITE,
        'bg_color': 185,
    },
    'white_text_pastel_deep_blue_bg': {
        'pair_num': 29,
        'text_color': COLOR_WHITE,
        'bg_color': 81,
    },
    'white_text_strong_magenta_bg': {
        'pair_num': 30,
        'text_color': COLOR_WHITE,
        'bg_color': 163,
    },
    'white_text_medium_grey_bg': {
        'pair_num': 31,
        'text_color': COLOR_WHITE,
        'bg_color': 8,
    },
    'white_text_bright_blue_green_bg': {
        'pair_num': 32,
        'text_color': COLOR_WHITE,
        'bg_color': 35,
    },
    'white_text_bright_pink_orange_bg': {
        'pair_num': 33,
        'text_color': COLOR_WHITE,
        'bg_color': 203,
    },
    'white_text_bright_pink_magenta_bg': {
        'pair_num': 34,
        'text_color': COLOR_WHITE,
        'bg_color': 205,
    },
    'white_text_bright_light_pastel_orange_bg': {
        'pair_num': 35,
        'text_color': COLOR_WHITE,
        'bg_color': 209,
    },
    'bright_white_text_bright_white_bg': {
        'pair_num': 36,
        'text_color': 255,
        'bg_color': 255,
    },
    'white_text_white_bg': {
        'pair_num': 37,
        'text_color': COLOR_WHITE,
        'bg_color': COLOR_WHITE,
    },
    'bright_white_text_black_bg': {
        'pair_num': 38,
        'text_color': 255,
        'bg_color': COLOR_BLACK,
    }
}
