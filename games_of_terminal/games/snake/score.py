from games_of_terminal.constants import MESSAGES

from pathlib import Path
import dotenv
import os


dotenv.load_dotenv()

FILENAME = '.env'
# FILENAME = 'games-of-terminal-settings.yml'
BASE_DIR = Path(__file__).parents[2]

FILE_PATH = os.path.join(BASE_DIR, FILENAME)


def get_best_score():
    if not os.path.exists(FILE_PATH):
        open(FILE_PATH, 'a').close()
        dotenv.set_key(FILE_PATH, 'SNAKE_BEST_SCORE', '0')

    best_score = dotenv.get_key(FILE_PATH, 'SNAKE_BEST_SCORE')
    return best_score


def save_best_score(score):
    best_score = get_best_score()
    if score > int(best_score):
        dotenv.set_key(FILE_PATH, 'SNAKE_BEST_SCORE', str(score))
        return True
    return False
