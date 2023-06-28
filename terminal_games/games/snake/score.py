from terminal_games.games.snake.common import MESSAGES
import os
import dotenv

dotenv.load_dotenv()

FILENAME = '.env'
CURRENT_DIR = os.getcwd()
FILE_PATH = os.path.join(CURRENT_DIR, FILENAME)


def show_score(stdscr, score):
    _, sw = stdscr.getmaxyx()
    score_text = MESSAGES['score_text'] + str(score)
    stdscr.addstr(1, sw // 2 - len(score_text) // 2, score_text)


def get_best_score():
    if not os.path.exists(FILE_PATH):
        open(FILE_PATH, 'a').close()
        dotenv.set_key(FILE_PATH, 'SNAKE_BEST_SCORE', '0')

    best_score = dotenv.get_key(FILE_PATH, 'SNAKE_BEST_SCORE')
    return best_score


def show_best_score(stdscr):
    _, sw = stdscr.getmaxyx()
    best_score = get_best_score()
    best_score_text = MESSAGES['best_score'] + str(best_score)
    stdscr.addstr(1, sw - len(best_score_text) - 3, best_score_text)


def save_best_score(score):
    best_score = get_best_score()
    if score > int(best_score):
        dotenv.set_key(FILE_PATH, 'SNAKE_BEST_SCORE', str(score))
        return True
    return False
