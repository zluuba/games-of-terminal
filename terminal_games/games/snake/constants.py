import curses


DIRECTIONS = {
    curses.KEY_RIGHT: curses.KEY_LEFT,
    curses.KEY_LEFT: curses.KEY_RIGHT,
    curses.KEY_UP: curses.KEY_DOWN,
    curses.KEY_DOWN: curses.KEY_UP,
}

KEYS = {
    'up_arrow': curses.KEY_UP,
    'down_arrow': curses.KEY_DOWN,
    'left_arrow': curses.KEY_LEFT,
    'right_arrow': curses.KEY_RIGHT,
    'space_btn': ord(' '),
    'esc_btn': 27,
}

MESSAGES = {
    'game_over': 'GAME OVER',
    'score_text': 'Score: ',
    'best_score': 'Best score: ',
    'new_best_score': 'New best score!',
    'start_text': 'Press any key to start',
    'play_again': 'Press Space to play again',
}

SNAKE_SKIN = 'O'
FOOD_SKIN = '×'
SKINS = ['#', 'O', '×', '¤', '■', '█', '≡', '©']
