from games_of_terminal.constants import (
    COLOR_MAPPING, COMMON_TIPS, DEFAULT_COLOR,
)

from curses import (
    start_color as init_start_color,
    color_pair,
    init_pair,
    curs_set,
)
from random import choice
from re import match


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
