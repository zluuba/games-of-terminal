from terminal_games.games.snake.common import MESSAGES
import os
import dotenv
# from pathlib import Path


dotenv.load_dotenv()

FILENAME = '.env'
BASE_DIR = os.getcwd()

# TODO: redo score saving
#       it's save in Python installing packages folder
#       or try not to use 'python3 -m pip install'

# FILENAME = 'term_games_scores.txt'
# BASE_DIR = Path(__file__).resolve().parent.parent

FILE_PATH = os.path.join(BASE_DIR, FILENAME)


def show_score(canvas, score, width):
    score_text = MESSAGES['score_text'] + str(score)
    y, x = 1, width // 2 - len(score_text) // 2
    canvas.addstr(y, x, score_text)


def get_best_score():
    if not os.path.exists(FILE_PATH):
        open(FILE_PATH, 'a').close()
        dotenv.set_key(FILE_PATH, 'SNAKE_BEST_SCORE', '0')

    best_score = dotenv.get_key(FILE_PATH, 'SNAKE_BEST_SCORE')
    return best_score


def show_best_score(canvas, width):
    best_score = get_best_score()
    best_score_text = MESSAGES['best_score'] + str(best_score)
    y, x = 1, width - len(best_score_text) - 3
    canvas.addstr(y, x, best_score_text)


def save_best_score(score):
    best_score = get_best_score()
    if score > int(best_score):
        dotenv.set_key(FILE_PATH, 'SNAKE_BEST_SCORE', str(score))
        return True
    return False
