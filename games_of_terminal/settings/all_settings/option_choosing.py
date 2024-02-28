from games_of_terminal.constants import KEYS, BASE_OFFSET, DEFAULT_COLOR
from games_of_terminal.database.database import save_selected_option
from games_of_terminal.interface_manager import InterfaceManager
from games_of_terminal.utils import (
    draw_message, clear_field_line, get_color_by_name,
    draw_colorful_message,
)
from .constants import (
    OPTIONS_CHOOSING_MSGS, OPTIONS_POST_MSG,
    LEFT_ARROW, RIGHT_ARROW, NO_ARROW,
)

from time import sleep


class OptionChoosing(InterfaceManager):
    def __init__(self, canvas, parent_class):
        super().__init__(canvas, only_main_win=True)

        self.parent_class = parent_class

        self.option_name = parent_class.current_option
        self.option_values = parent_class.current_option_values

        self.curr_option_ind = 0
        self.setup_vars()

    def setup_vars(self):
        self.height, self.width = self.canvas.getmaxyx()

        self.text_start_y = self.get_text_start_y()
        self.options_start_y = self.get_options_start_y()

    def get_text_start_y(self):
        return ((self.height // 2) -
                ((len(OPTIONS_CHOOSING_MSGS) + BASE_OFFSET + 1) // 2))

    def get_options_start_y(self):
        return self.text_start_y + len(OPTIONS_CHOOSING_MSGS) + BASE_OFFSET

    def get_option_max_name_length(self):
        return max(map(lambda opt: len(opt['name']), self.option_values))

    @property
    def current_option_name(self):
        return self.option_values[self.curr_option_ind]['name']

    @property
    def is_current_option_selected(self):
        return self.option_values[self.curr_option_ind]['selected']

    @property
    def is_curr_option_is_first(self):
        return self.curr_option_ind == 0

    @property
    def is_curr_option_is_last(self):
        return self.curr_option_ind == len(self.option_values) - 1

    def run(self):
        self.draw_option_choosing_window()

        while True:
            key = self.window.getch()
            self.wait_for_keypress()

            if key == KEYS['escape']:
                return
            elif key == KEYS['resize']:
                self.window.timeout(0)
                self.resize_menu_win_handler(key)
            elif key in KEYS['enter']:
                save_selected_option(
                    self.parent_class.chosen_game_name,
                    self.option_name, self.current_option_name
                )
                self.draw_post_editing_text()
                return
            elif key in (KEYS['left_arrow'], KEYS['a']):
                self.moving_controller('left')
            elif key in (KEYS['right_arrow'], KEYS['d']):
                self.moving_controller('right')

    def moving_controller(self, direction):
        offset = 1 if direction == 'right' else -1
        new_option_ind = self.curr_option_ind + offset

        if new_option_ind < 0 or new_option_ind >= len(self.option_values):
            return

        self.clear_option_choosing_field()
        self.curr_option_ind = new_option_ind
        self.draw_option_choosing_field()
        self.draw_arrows_around_option()

    def draw_option_choosing_window(self):
        self.window.clear()
        self.draw_option_name()
        self.draw_tips_text()
        self.draw_option_choosing_field()
        self.draw_arrows_around_option()

    def draw_option_name(self):
        color = get_color_by_name('yellow_text_black_bg')
        prettify_name = self.parent_class.prettify_option(self.option_name)
        y = self.text_start_y - BASE_OFFSET
        x = (self.width // 2) - (len(self.option_name) // 2)

        draw_message(y, x, self.window, prettify_name, color)

    def draw_tips_text(self):
        color = get_color_by_name('grey_text_black_bg')

        for row, message in enumerate(OPTIONS_CHOOSING_MSGS):
            y = self.text_start_y + row
            x = (self.width // 2) - (len(message) // 2)

            draw_message(y, x, self.window, message, color)

    def draw_option_choosing_field(self):
        text = self.current_option_name
        color = get_color_by_name('bright_white_text_black_bg')
        y = self.options_start_y

        if self.is_current_option_selected:
            text = (
                (self.current_option_name, color),
                (' (selected)', DEFAULT_COLOR),
            )
            draw_colorful_message(y, self.width,
                                  self.window, text)
        else:
            x = max(1, (self.width // 2) - (len(text) // 2))

            draw_message(y, x, self.window, text, color)

    def clear_option_choosing_field(self):
        option_length = len(self.current_option_name)
        option_length += len(' (selected)') if self.is_current_option_selected else 0

        y = self.options_start_y
        x = max(1, (self.width // 2) - (option_length // 2))

        clear_field_line(y, x, self.window, option_length)

    def draw_arrows_around_option(self):
        max_len_name = self.get_option_max_name_length() + len(' (selected)')

        left_arrow_x = ((self.width // 2) -
                        (max_len_name // 2) -
                        BASE_OFFSET)
        right_arrow_x = left_arrow_x + (BASE_OFFSET * 2) + max_len_name - 1

        left_arrow = NO_ARROW if self.is_curr_option_is_first else LEFT_ARROW
        right_arrow = NO_ARROW if self.is_curr_option_is_last else RIGHT_ARROW

        draw_message(self.options_start_y, left_arrow_x,
                     self.window, left_arrow)
        draw_message(self.options_start_y, right_arrow_x,
                     self.window, right_arrow)

    def draw_post_editing_text(self):
        self.window.clear()

        y = self.height // 2
        x = (self.width // 2) - (len(OPTIONS_POST_MSG) // 2)

        draw_message(y, x, self.window, OPTIONS_POST_MSG)
        sleep(1)

    def redraw_window(self):
        self.setup_vars()
        self.draw_option_choosing_window()
