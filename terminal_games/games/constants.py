import curses


LOGO = [
    '######  #####  #####   ##   ##',
    '  ##    ##     ##  ##  ### ###',
    '  ##    ####   ####    ## # ##',
    '  ##    ##     ## ##   ##   ##',
    '  ##    #####  ##  ##  ##   ##',
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
}

GAME_STATUSES = {
    'user_win': 'You WIN!',
    'computer_win': 'You LOSE.',
    'tie': 'Tie. Meh.',
}

SIDE_MENU_TIPS = [
    'Rules     - r',
    'Move      - ← ↓ ↑ →',
    'Quit      - q',
    'Pause     - p',
    'Hide tips - h',
]
