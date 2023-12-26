from curses import (
    start_color, color_pair, init_pair,
    COLOR_WHITE, COLOR_BLACK, COLOR_GREEN,
    COLOR_RED, COLOR_YELLOW,
)

from random import choice
from re import match


class Colors:
    def __init__(self):
        self.color_mapping = {
            'white_text_black_bg': 0,
            'white_text_green_bg': 1,
            'white_text_red_bg': 2,
            'white_text_dark_grey_bg': 3,
            'white_text_light_grey_bg': 4,
            'white_text_pink_bg': 5,
            'white_text_light_purple_bg': 6,

            'red_text_black_bg': 7,
            'green_text_black_bg': 8,
            'yellow_text_black_bg': 9,

            'black_text_red_bg': 10,
            'black_text_deep_pink_bg': 11,
            'black_text_pastel_dirty_blue_bg': 12,

            'white_text_pastel_blue_bg': 13,
            'white_text_light_blue_bg': 14,
            'white_text_medium_blue_bg': 15,
            'white_text_dark_medium_blue_bg': 16,
            'white_text_deep_blue_bg': 17,
            'white_text_deep_purple_bg': 18,

            'white_text_yellow_bg': 19,
            'strong_pastel_purple_text_black_bg': 20,
            'light_grey_text_black_bg': 21,

            'white_text_light_black_bg': 22,
            'light_black_text_black_bg': 23,
            'very_light_grey_text_black_bg': 24,
            'grey_text_black_bg': 25,

            'white_text_bright_light_orange_bg': 26,
            'white_text_peaceful_red_bg': 27,
            'white_text_pastel_yellow_bg': 28,
            'white_text_pastel_deep_blue_bg': 29,
            'white_text_strong_magenta_bg': 30,
        }

        start_color()

        init_pair(1, COLOR_WHITE, COLOR_GREEN)
        init_pair(2, COLOR_WHITE, COLOR_RED)
        init_pair(3, COLOR_WHITE, 236)
        init_pair(4, COLOR_WHITE, 245)
        init_pair(5, COLOR_WHITE, 132)
        init_pair(6, COLOR_WHITE, 134)

        init_pair(7, COLOR_RED, COLOR_BLACK)
        init_pair(8, COLOR_GREEN, COLOR_BLACK)
        init_pair(9, COLOR_YELLOW, COLOR_BLACK)

        init_pair(10, COLOR_BLACK, COLOR_RED)
        init_pair(11, COLOR_BLACK, 168)
        init_pair(12, COLOR_BLACK, 153)

        # minesweeper cell colors
        init_pair(13, COLOR_WHITE, 111)
        init_pair(14, COLOR_WHITE, 75)
        init_pair(15, COLOR_WHITE, 68)
        init_pair(16, COLOR_WHITE, 26)
        init_pair(17, COLOR_WHITE, 17)
        init_pair(18, COLOR_WHITE, 54)

        init_pair(19, COLOR_WHITE, 136)
        init_pair(20, 147, COLOR_BLACK)
        init_pair(21, 245, COLOR_BLACK)

        init_pair(22, COLOR_WHITE, 232)
        init_pair(23, 233, COLOR_BLACK)
        init_pair(24, 248, COLOR_BLACK)
        init_pair(25, 242, COLOR_BLACK)

        init_pair(26, COLOR_WHITE, 208)
        init_pair(27, COLOR_WHITE, 124)
        init_pair(28, COLOR_WHITE, 185)
        init_pair(29, COLOR_WHITE, 81)
        init_pair(30, COLOR_WHITE, 163)

        self.default_color = self.get_color_by_name('white_text_black_bg')
        self.game_state_color = self.get_color_by_name('strong_pastel_purple_text_black_bg')

    def get_color_by_name(self, color_name):
        color_pair_number = self.color_mapping.get(color_name, 0)
        return color_pair(color_pair_number)

    def get_random_colored_background(self):
        colored_bg_names = list(filter(
            lambda color: match(r'.+(?=(?<!black_bg)(?<!grey_bg))$', color),
            list(self.color_mapping)
        ))

        random_color_name = choice(colored_bg_names)
        return random_color_name
