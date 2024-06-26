from games_of_terminal.constants import (
    COLOR_MAPPING, COMMON_TIPS, DEFAULT_COLOR,
    MIN_WIN_HEIGHT, MIN_WIN_WIDTH, DEFAULT_STUB_MSG,
    TERM_RED_COLOR, TERM_DEFAULT_COLOR,
)
from games_of_terminal.database.database import (
    update_game_stat,
    get_game_settings,
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

from ast import literal_eval
from collections import defaultdict


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
        list(COLOR_MAPPING),
    ))

    random_color_name = choice(colored_bg_names)
    return random_color_name


def hide_cursor():
    curs_set(0)


def show_cursor():
    curs_set(2)


def is_user_press_key(key):
    return key != -1


def draw_message(y, x, field, message, color=DEFAULT_COLOR):
    field.addstr(y, x, message, color)
    field.refresh()


def draw_colorful_message(y, win_width, field, message_with_colors):
    message_len = sum(map(lambda pair: len(pair[0]), message_with_colors))
    x = (win_width // 2) - (message_len // 2)

    for message, color in message_with_colors:
        draw_message(y, x, field, message, color)
        x += len(message)


def clear_field_line(begin_y, begin_x, field, width):
    empty_line = ' ' * width
    draw_message(begin_y, begin_x, field, empty_line)


def handle_accidentally_key_pressing():
    sleep(0.3)
    flushinp()


def too_small_window_handler(height, width):
    error_message = 'ERROR: Window is too small.\n'
    req_msg = f'Minimum height: {MIN_WIN_HEIGHT}, width: {MIN_WIN_WIDTH}.\n'
    curr_msg = f'Current height: {height}, width: {width}.'

    if (height < MIN_WIN_HEIGHT) or (width < MIN_WIN_WIDTH):
        exit(TERM_RED_COLOR + error_message +
             TERM_DEFAULT_COLOR + req_msg + curr_msg)


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


def show_placeholder_stub(height, width, window, message=DEFAULT_STUB_MSG):
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


def get_current_color_scheme_name(color_schemes):
    for scheme in color_schemes:
        if scheme['selected']:
            return scheme['name']
    return ''


def is_current_setting_option_is_default(settings):
    for option in settings:
        if option['selected']:
            return 'default' in option
    return False


def get_prettified_game_settings(game_name):
    game_settings_db_data = get_game_settings(game_name)
    game_settings = defaultdict(dict)

    for settings in game_settings_db_data:
        setting_name, setting_value = settings

        if setting_value and (not setting_name == 'username'):
            setting_value = literal_eval(setting_value)

        game_settings[setting_name] = setting_value

    return game_settings
