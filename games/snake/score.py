from common import MESSAGES
import os


def print_score(stdscr, score):
    _, sw = stdscr.getmaxyx()
    score_text = MESSAGES['score_text'] + str(score)
    stdscr.addstr(1, sw // 2 - len(score_text) // 2, score_text)


def print_best_score(stdscr):
    """
    - add storage for files like this and put best score on it
    """
    _, sw = stdscr.getmaxyx()
    filename = 'best_score.txt'
    directory = os.getcwd()
    file_path = os.path.join(directory, filename)
    if not os.path.exists(file_path):
        open(file_path, 'a').write('0')
    best_score = open(file_path, 'r').read()
    best_score_text = MESSAGES['best_score'] + str(best_score)
    stdscr.addstr(1, sw - len(best_score_text) - 3, best_score_text)


def save_best_score(score):
    filename = 'best_score.txt'
    directory = os.getcwd()
    file_path = os.path.join(directory, filename)
    best_score = open(file_path, 'r').read()
    if score > int(best_score):
        open(file_path, 'w').write(str(score))
        return True
    return False
