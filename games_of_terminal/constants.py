import curses


APP_NAME = 'Games Of Terminal'

LOGO = [
    ' ####     ####   ######',
    '##       ##  ##    ##  ',
    '##  ###  ##  ##    ##  ',
    '##   ##  ##  ##    ##  ',
    ' #####    ####     ##  ',
]

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
    'enter': [curses.KEY_ENTER, 10, 13],
    'up_arrow': curses.KEY_UP,
    'down_arrow': curses.KEY_DOWN,
    'left_arrow': curses.KEY_LEFT,
    'right_arrow': curses.KEY_RIGHT,
    'q': ord('q'),
    'pause': ord('p'),
    # 'w': ord('w'),
    # 's': ord('s'),
    # 'a': ord('a'),
    # 'd': ord('d'),
}

GAME_STATUSES = {
    'user_win': {'text': 'You WIN!', 'color': 'white_text_green_bg'},
    'user_lose': {'text': 'You LOSE', 'color': 'white_text_red_bg'},
    'tie': {'text': 'TIE', 'color': 'white_text_yellow_bg'},
}

SIDE_MENU_TIPS = {
    'Move': '← ↓ ↑ → (wasd)',
    'Pause': 'p',
    'Restart': 'r',
    'Tips/rules': 't',
    'Quit': 'q',
    'Hide menu': 'm',
}
