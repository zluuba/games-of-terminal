import curses


CURSES_DIRECTIONS = [
    curses.KEY_RIGHT, curses.KEY_LEFT,
    curses.KEY_UP, curses.KEY_DOWN,
]

OPPOSITE_DIRECTIONS = {
    curses.KEY_RIGHT: curses.KEY_LEFT, curses.KEY_LEFT: curses.KEY_RIGHT,
    curses.KEY_UP: curses.KEY_DOWN, curses.KEY_DOWN: curses.KEY_UP,
}

MESSAGES = {
    'game_over': 'GAME OVER',
    'score_text': 'Score: ',
    'best_score': 'Best score: ',
    'new_best_score': 'New best score!',
    'start_text': 'Press any key to start',
    'play_again': 'Press Space to play again',
}
