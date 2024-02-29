from curses import (
    KEY_ENTER, KEY_UP, KEY_DOWN,
    KEY_LEFT, KEY_RIGHT, KEY_RESIZE,
    KEY_BACKSPACE,
    COLOR_WHITE, COLOR_BLACK, COLOR_GREEN,
    COLOR_RED, COLOR_YELLOW,
)


APP_NAME = 'Games Of Terminal'

LOGO = [
    ' ▒▒▒▒    ▒▒▒▒  ▒▒▒▒▒▒',
    '▒▒      ▒▒  ▒▒   ▒▒  ',
    '▒▒ ▒▒▒  ▒▒  ▒▒   ▒▒  ',
    '▒▒  ▒▒  ▒▒  ▒▒   ▒▒  ',
    ' ▒▒▒▒    ▒▒▒▒    ▒▒  ',
]

OLD_LOGO = [
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

ACH_TEXT = 'ACHIEVEMENT UNLOCKED'
ACH_FRAME_COLOR_NAME = 'purple_text_black_bg'
ACH_NAME_COLOR_NAME = 'bright_white_text_black_bg'
ACH_BG_COLOR_NAME = 'bright_light_pastel_orange_text_black_bg'

KEYS = {
    'up_arrow': KEY_UP,
    'down_arrow': KEY_DOWN,
    'left_arrow': KEY_LEFT,
    'right_arrow': KEY_RIGHT,
    'enter': (KEY_ENTER, 10, 13),
    'delete': (KEY_BACKSPACE, '\b', '\x7f', 127),
    'tab': (ord('\t'), 9),
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
    'x': ord('x'),
}

GAMES = [
    'Snake',
    'Minesweeper',
    'Tic Tac Toe',
    'Tetris',
]

ITEMS = [
    'Global',
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
    'pause': 'PAUSE',
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
    'Settings': 'X',
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
    },
    'green_text_white_bg': {
        'pair_num': 39,
        'text_color': COLOR_GREEN,
        'bg_color': COLOR_WHITE,
    },
    'strong_red_text_black_bg': {
        'pair_num': 40,
        'text_color': 160,
        'bg_color': COLOR_BLACK,
    },
    'purple_text_black_bg': {
        'pair_num': 41,
        'text_color': 177,
        'bg_color': COLOR_BLACK,
    },
    'light_blue_text_black_bg': {
        'pair_num': 42,
        'text_color': 75,
        'bg_color': COLOR_BLACK,
    },
    'dark_medium_blue_text_black_bg': {
        'pair_num': 43,
        'text_color': 26,
        'bg_color': COLOR_BLACK,
    },
    'black_text_dark_orange_bg': {
        'pair_num': 44,
        'text_color': COLOR_BLACK,
        'bg_color': 130,
    },
    'black_text_pastel_light_peach_bg': {
        'pair_num': 45,
        'text_color': COLOR_BLACK,
        'bg_color': 180,
    },
    'black_text_light_pastel_purple_bg': {
        'pair_num': 46,
        'text_color': COLOR_BLACK,
        'bg_color': 146,
    },
    'black_text_light_pastel_lettuce_bg': {
        'pair_num': 47,
        'text_color': COLOR_BLACK,
        'bg_color': 151,
    },
    'black_text_light_lettuce_bg': {
        'pair_num': 48,
        'text_color': COLOR_BLACK,
        'bg_color': 149,
    },
    'black_text_peach_bg': {
        'pair_num': 49,
        'text_color': COLOR_BLACK,
        'bg_color': 174,
    },
    'black_text_peaceful_strong_purple_bg': {
        'pair_num': 50,
        'text_color': COLOR_BLACK,
        'bg_color': 129,
    },
    'white_text_light_grey_brighter_v2_bg': {
        'pair_num': 51,
        'text_color': COLOR_WHITE,
        'bg_color': 247,
    },
    'white_text_grey_brighter_v1_bg': {
        'pair_num': 52,
        'text_color': COLOR_WHITE,
        'bg_color': 243,
    },
    'white_text_medium_grey_brighter_v1_bg': {
        'pair_num': 53,
        'text_color': COLOR_WHITE,
        'bg_color': 239,
    },
    'black_text_grey_white_brighter_v3_bg': {
        'pair_num': 54,
        'text_color': COLOR_BLACK,
        'bg_color': 254,
    },
    'black_text_very_light_grey_brighter_v1_bg': {
        'pair_num': 55,
        'text_color': COLOR_BLACK,
        'bg_color': 249,
    },
    'white_text_dark_grey_brighter_v2_bg': {
        'pair_num': 56,
        'text_color': COLOR_WHITE,
        'bg_color': 237,
    },
    'very_bright_dull_pastel_yellow_green_text_black_bg': {
        'pair_num': 57,
        'text_color': 193,
        'bg_color': COLOR_BLACK,
    },
    'strong_pastel_blue_text_black_bg': {
        'pair_num': 58,
        'text_color': 111,
        'bg_color': COLOR_BLACK,
    },
    'pastel_light_peach_text_black_bg': {
        'pair_num': 59,
        'text_color': 180,
        'bg_color': COLOR_BLACK,
    },
    'very_bright_yellow_text_black_bg': {
        'pair_num': 60,
        'text_color': 220,
        'bg_color': COLOR_BLACK,
    },
    'pastel_dirty_blue_text_black_bg': {
        'pair_num': 61,
        'text_color': 153,
        'bg_color': COLOR_BLACK,
    },
    'white_text_black_bg': {
        'pair_num': 62,
        'text_color': COLOR_WHITE,
        'bg_color': COLOR_BLACK,
    },
    'pastel_brown_red_text_black_bg': {
        'pair_num': 63,
        'text_color': 95,
        'bg_color': COLOR_BLACK,
    },
    'black_text_white_bg': {
        'pair_num': 64,
        'text_color': COLOR_BLACK,
        'bg_color': COLOR_WHITE,
    },
    'black_text_deep_green_bg': {
        'pair_num': 65,
        'text_color': COLOR_BLACK,
        'bg_color': 22,
    },
    'black_text_very_bright_light_pastel_pink_bg': {
        'pair_num': 66,
        'text_color': COLOR_BLACK,
        'bg_color': 217,
    },
    'black_text_very_bright_pastel_light_yellow_v2_bg': {
        'pair_num': 67,
        'text_color': COLOR_BLACK,
        'bg_color': 229,
    },
    'black_text_aqua_light_blue_bg': {
        'pair_num': 68,
        'text_color': COLOR_BLACK,
        'bg_color': 24,
    },
    'black_text_medium_aqua_light_blue_bg': {
        'pair_num': 69,
        'text_color': COLOR_BLACK,
        'bg_color': 38,
    },
    'black_text_bright_white_bg': {
        'pair_num': 70,
        'text_color': COLOR_BLACK,
        'bg_color': 255,
    },
}
