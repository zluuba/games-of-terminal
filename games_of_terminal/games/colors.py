import curses


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
        }

        curses.start_color()

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(4, curses.COLOR_WHITE, 236)
        curses.init_pair(5, curses.COLOR_WHITE, 245)
        curses.init_pair(6, curses.COLOR_WHITE, 132)
        curses.init_pair(7, curses.COLOR_WHITE, 134)

        curses.init_pair(8, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(9, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(10, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(12, curses.COLOR_BLACK, 168)
        curses.init_pair(13, curses.COLOR_BLACK, 153)

        # minesweeper cell colors
        curses.init_pair(14, curses.COLOR_WHITE, 111)
        curses.init_pair(15, curses.COLOR_WHITE, 75)
        curses.init_pair(16, curses.COLOR_WHITE, 68)
        curses.init_pair(17, curses.COLOR_WHITE, 26)
        curses.init_pair(18, curses.COLOR_WHITE, 17)
        curses.init_pair(19, curses.COLOR_WHITE, 54)

    def get_color_by_name(self, color_name):
        color_pair = self.color_mapping.get(color_name, 0)
        return curses.color_pair(color_pair)
