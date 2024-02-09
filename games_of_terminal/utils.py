from games_of_terminal.constants import (
    COLOR_MAPPING, COMMON_TIPS, DEFAULT_COLOR,
    MIN_WIN_HEIGHT, MIN_WIN_WIDTH,
)
from games_of_terminal.database.database import (
    update_game_stat,
)

from curses import (
    start_color as init_start_color,
    color_pair,
    init_pair,
    curs_set,
    flushinp,
)
from random import choice
from re import match
from sys import exit
from time import time, sleep


def init_curses_colors():
    init_start_color()

    for color in COLOR_MAPPING.values():
        pair_num = color['pair_num']
        text_color = color['text_color']
        bg_color = color['bg_color']

        init_pair(pair_num, text_color, bg_color)


def get_color_by_name(color_name):
    if color_name not in COLOR_MAPPING:
        return 0

    color = COLOR_MAPPING[color_name]
    color_pair_number = color['pair_num']
    return color_pair(color_pair_number)


def get_random_colored_background():
    re_pattern = r'.+(?=(?<!black_bg)(?<!grey_bg))$'
    colored_bg_names = list(filter(
        lambda color_name: match(re_pattern, color_name),
        list(COLOR_MAPPING)
    ))

    random_color_name = choice(colored_bg_names)
    return random_color_name


def hide_cursor():
    curs_set(0)


def draw_message(begin_y, begin_x, field, message, color=DEFAULT_COLOR):
    field.addstr(begin_y, begin_x, message, color)
    field.refresh()


def clear_field_line(begin_y, begin_x, field, width):
    empty_line = ' ' * width
    draw_message(begin_y, begin_x, field, empty_line)


def handle_accidentally_key_pressing():
    sleep(0.3)
    flushinp()


def too_small_window_handler(height, width):
    red_color = '\033[91m'
    default_color = '\033[39m'

    error_message = f'ERROR: Window is too small.\n'
    req_msg = f'Minimum height: {MIN_WIN_HEIGHT}, width: {MIN_WIN_WIDTH}.\n'
    curr_msg = f'Current height: {height}, width: {width}.'

    if (height < MIN_WIN_HEIGHT) or (width < MIN_WIN_WIDTH):
        exit(red_color + error_message +
             default_color + req_msg + curr_msg)


def get_side_menu_tips(game_state, game_tips):
    return [
        {
            'name': 'state',
            'tips': game_state,
            'color': get_color_by_name('strong_pastel_purple_text_black_bg'),
        },
        {
            'name': 'game_tips',
            'tips': game_tips,
            'color': DEFAULT_COLOR,
        },
        {
            'name': 'common',
            'tips': COMMON_TIPS,
            'color': DEFAULT_COLOR,
        }
    ]


def show_placeholder_stub(height, width, window,
                          message='In development.'):
    y = height // 2
    x = (width // 2) - (len(message) // 2)

    window.clear()
    draw_message(y, x, window, message, DEFAULT_COLOR)


def update_total_games_count(game_name, value):
    update_game_stat(game_name, 'total_games', value)


def update_total_time_count(game_name, start_time):
    end_time = time()
    time_in_game = int(end_time - start_time)
    update_game_stat(game_name, 'total_time', time_in_game)


def update_best_score(game_name, score):
    update_game_stat(game_name, 'best_score', score, save_mode=True)
