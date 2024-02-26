from games_of_terminal.constants import KEYS, BASE_OFFSET, DEFAULT_COLOR
from games_of_terminal.database.database import save_selected_option
from games_of_terminal.utils import (
    draw_message, clear_field_line, get_color_by_name,
    draw_colorful_message,
)
from .constants import (
    OPTIONS_CHOOSING_MSGS,
    LEFT_ARROW, RIGHT_ARROW, NO_ARROW,
)


class OptionChoosing:
    def __init__(self, parent_class):
        self.parent_class = parent_class

        self.option_name = parent_class.current_option
        self.option_values = parent_class.current_option_values

        self.text_start_y = self.get_text_start_y()
        self.options_start_y = self.get_options_start_y()

        self.curr_option_ind = 0

    def get_text_start_y(self):
        return ((self.parent_class.height // 2) -
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
            key = self.parent_class.window.getch()
            self.parent_class.wait_for_keypress()

            if key == KEYS['escape']:
                return
            elif key in KEYS['enter']:
                save_selected_option(self.parent_class.chosen_game_name,
                                     self.option_name, self.current_option_name)
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
        self.parent_class.window.clear()
        self.draw_option_name()
        self.draw_tips_text()
        self.draw_option_choosing_field()
        self.draw_arrows_around_option()

    def draw_option_name(self):
        color = get_color_by_name('yellow_text_black_bg')
        prettify_name = self.parent_class.prettify_option(self.option_name)
        y = self.text_start_y - BASE_OFFSET
        x = (self.parent_class.width // 2) - (len(self.option_name) // 2)

        draw_message(y, x, self.parent_class.window, prettify_name, color)

    def draw_tips_text(self):
        color = get_color_by_name('grey_text_black_bg')

        for row, message in enumerate(OPTIONS_CHOOSING_MSGS):
            y = self.text_start_y + row
            x = (self.parent_class.width // 2) - (len(message) // 2)

            draw_message(y, x, self.parent_class.window, message, color)

    def draw_option_choosing_field(self):
        text = self.current_option_name
        color = get_color_by_name('bright_white_text_black_bg')
        y = self.options_start_y

        if self.is_current_option_selected:
            text = (
                (self.current_option_name, color),
                (' (selected)', DEFAULT_COLOR),
            )
            draw_colorful_message(y, self.parent_class.width,
                                  self.parent_class.window, text)
        else:
            x = max(1, (self.parent_class.width // 2) - (len(text) // 2))

            draw_message(y, x, self.parent_class.window, text, color)

    def clear_option_choosing_field(self):
        option_length = len(self.current_option_name)
        option_length += len(' (selected)') if self.is_current_option_selected else 0

        y = self.options_start_y
        x = max(1, (self.parent_class.width // 2) - (option_length // 2))

        clear_field_line(y, x, self.parent_class.window, option_length)

    def draw_arrows_around_option(self):
        max_len_name = self.get_option_max_name_length() + len(' (selected)')

        left_arrow_x = ((self.parent_class.width // 2) -
                        (max_len_name // 2) -
                        BASE_OFFSET)
        right_arrow_x = left_arrow_x + (BASE_OFFSET * 2) + max_len_name - 1

        left_arrow = NO_ARROW if self.is_curr_option_is_first else LEFT_ARROW
        right_arrow = NO_ARROW if self.is_curr_option_is_last else RIGHT_ARROW

        draw_message(self.options_start_y, left_arrow_x,
                     self.parent_class.window, left_arrow)
        draw_message(self.options_start_y, right_arrow_x,
                     self.parent_class.window, right_arrow)
