from games_of_terminal.constants import (
    COLOR_MAPPING, COMMON_TIPS, DEFAULT_COLOR,
    MIN_WIN_HEIGHT, MIN_WIN_WIDTH,
)

from curses import (
    start_color as init_start_color,
    color_pair,
    init_pair,
    curs_set,
)
from random import choice
from re import match
from sys import exit


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


def draw_message(begin_y, begin_x, field, message, color):
    field.addstr(begin_y, begin_x, message, color)
    field.refresh()


def clear_field_line(begin_y, begin_x, field, width):
    empty_line = ' ' * width
    draw_message(begin_y, begin_x, field, empty_line, DEFAULT_COLOR)


def too_small_window_handler(height, width):
    red_color = '\033[91m'
    default_color = '\033[39m'

    error_message = f'ERROR: Window is too small.\n'
    req_msg = f'Minimum height: {MIN_WIN_HEIGHT}, width: {MIN_WIN_WIDTH}.\n'
    curr_msg = f'Current height: {height}, width: {width}.'

    if (height < MIN_WIN_HEIGHT) or (width < MIN_WIN_WIDTH):
        exit(red_color + error_message +
             default_color + req_msg + curr_msg)


def get_game_tips(game_state, game_tips):
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
                          color, message='In development.'):
    y = height // 2
    x = (width // 2) - (len(message) // 2)

    window.clear()
    draw_message(y, x, window, message, color)
