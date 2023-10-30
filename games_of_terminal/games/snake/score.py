from dotenv import load_dotenv, set_key, get_key
from pathlib import Path
from os import path


load_dotenv()

FILENAME = '.env'
# FILENAME = 'games-of-terminal-settings.yml'
BASE_DIR = Path(__file__).parents[2]

FILE_PATH = path.join(BASE_DIR, FILENAME)


def get_best_score():
    if not path.exists(FILE_PATH):
        open(FILE_PATH, 'a').close()
        set_key(FILE_PATH, 'SNAKE_BEST_SCORE', '0')

    best_score = get_key(FILE_PATH, 'SNAKE_BEST_SCORE')
    return best_score


def save_best_score(score):
    best_score = get_best_score()
    if score > int(best_score):
        set_key(FILE_PATH, 'SNAKE_BEST_SCORE', str(score))
        return True
    return False
