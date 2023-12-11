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
            'white_text_black_bg': 1,
            'white_text_green_bg': 2,
            'white_text_red_bg': 3,
            'white_text_dark_grey_bg': 4,
            'white_text_light_grey_bg': 5,
            'white_text_pink_bg': 6,
            'white_text_light_purple_bg': 7,

            'red_text_black_bg': 8,
            'green_text_black_bg': 9,
            'yellow_text_black_bg': 10,

            'black_text_red_bg': 11,
            'black_text_deep_pink_bg': 12,
            'black_text_pastel_dirty_blue_bg': 13,

            'white_text_pastel_blue_bg': 14,
            'white_text_light_blue_bg': 15,
            'white_text_medium_blue_bg': 16,
            'white_text_dark_medium_blue_bg': 17,
            'white_text_deep_blue_bg': 18,
            'white_text_deep_purple_bg': 19,

            'white_text_yellow_bg': 20,
            'strong_pastel_purple_text_black_bg': 21,
            'light_grey_text_black_bg': 22,

            'white_text_light_black_bg': 23,
            'light_black_text_black_bg': 24,
            'very_light_grey_text_black_bg': 25,
            'grey_text_black_bg': 26,
        }

        start_color()

        init_pair(1, COLOR_WHITE, COLOR_BLACK)
        init_pair(2, COLOR_WHITE, COLOR_GREEN)
        init_pair(3, COLOR_WHITE, COLOR_RED)
        init_pair(4, COLOR_WHITE, 236)
        init_pair(5, COLOR_WHITE, 245)
        init_pair(6, COLOR_WHITE, 132)
        init_pair(7, COLOR_WHITE, 134)

        init_pair(8, COLOR_RED, COLOR_BLACK)
        init_pair(9, COLOR_GREEN, COLOR_BLACK)
        init_pair(10, COLOR_YELLOW, COLOR_BLACK)

        init_pair(11, COLOR_BLACK, COLOR_RED)
        init_pair(12, COLOR_BLACK, 168)
        init_pair(13, COLOR_BLACK, 153)

        # minesweeper cell colors
        init_pair(14, COLOR_WHITE, 111)
        init_pair(15, COLOR_WHITE, 75)
        init_pair(16, COLOR_WHITE, 68)
        init_pair(17, COLOR_WHITE, 26)
        init_pair(18, COLOR_WHITE, 17)
        init_pair(19, COLOR_WHITE, 54)

        init_pair(20, COLOR_WHITE, 136)
        init_pair(21, 147, COLOR_BLACK)
        init_pair(22, 245, COLOR_BLACK)

        init_pair(23, COLOR_WHITE, 232)
        init_pair(24, 233, COLOR_BLACK)
        init_pair(25, 248, COLOR_BLACK)
        init_pair(26, 242, COLOR_BLACK)

        self.default_color = self.get_color_by_name('white_text_black_bg')

    def get_color_by_name(self, color_name):
        color_pair_number = self.color_mapping.get(color_name, 0)
        return color_pair(color_pair_number)

    def get_random_colored_background(self):
        colored_bg_names = list(filter(
            lambda color: match(r".*(?<!black_bg)$", color),
            list(self.color_mapping)
        ))
        random_color_name = choice(colored_bg_names)
        return self.get_color_by_name(random_color_name)
