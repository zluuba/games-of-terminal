from games_of_terminal.constants import KEYS, DEFAULT_COLOR
from games_of_terminal.database.database import reset_all_user_data
from games_of_terminal.interface_manager import InterfaceManager
from games_of_terminal.utils import (
    draw_message, handle_accidentally_key_pressing,
)
from games_of_terminal.settings.reset_all.constants import (
    TEXT, OPTIONS, BASE_OFFSET, OPTIONS_OFFSET,
)

from curses import A_STANDOUT as REVERSE
from time import sleep


class ResetAll(InterfaceManager):
    def __init__(self, canvas, name):
        super().__init__(canvas, only_main_win=True)

        self.name = name
        self.setup_vars()

    def setup_vars(self):
        self.position = 0

        self.text_len = len(TEXT)
        self.text_begin_y = self.get_text_begin_y()

        self.options_len = len(OPTIONS)
        self.options_begin_y = self.text_begin_y + self.text_len + BASE_OFFSET
        self.options_begin_x = self.get_options_begin_x()

    def get_text_begin_y(self):
        return (self.height - BASE_OFFSET - self.text_len) // 2

    def get_options_begin_x(self):
        all_options_length = self.get_all_options_line_length()
        return (self.width // 2) - (all_options_length // 2)

    @staticmethod
    def get_all_options_line_length():
        return sum(map(
            lambda option: len(option) + OPTIONS_OFFSET,
            OPTIONS.keys(),
        ))

    def get_selected_option(self):
        all_options = list(OPTIONS.keys())
        return all_options[self.position]

    def run(self):
        self.initialize_settings()
        handle_accidentally_key_pressing()

        while True:
            key = self.window.getch()
            self.wait_for_keypress()

            if key == KEYS['escape']:
                return
            elif key == KEYS['resize']:
                self.window.timeout(0)
                self.resize_menu_win_handler(key)
            elif key in (KEYS['left_arrow'], KEYS['a']):
                self.update_position(-1)
            elif key in (KEYS['right_arrow'], KEYS['d']):
                self.update_position(1)
            elif key in KEYS['enter']:
                self.handling_user_selection()
                return

    def initialize_settings(self):
        self.show_reset_all_main_text()
        self.show_options()

    def update_position(self, value):
        new_position = self.position + value

        if new_position < 0:
            new_position = self.options_len - 1
        elif new_position > self.options_len - 1:
            new_position = 0

        self.position = new_position
        self.show_options()

    def handling_user_selection(self):
        user_selection = self.get_selected_option()

        if user_selection == 'yes':
            reset_all_user_data()

        self.draw_option_selection_animation()
        self.show_option_text(user_selection)

    def show_reset_all_main_text(self):
        for row, sentence in enumerate(TEXT):
            begin_y = self.text_begin_y + row
            begin_x = (self.width // 2) - (len(sentence) // 2)

            draw_message(begin_y, begin_x, self.window, sentence)

    def show_options(self):
        begin_x = self.options_begin_x

        for index, option in enumerate(OPTIONS.keys()):
            color = DEFAULT_COLOR

            if index == self.position:
                color += REVERSE

            draw_message(self.options_begin_y, begin_x,
                         self.window, option, color)
            begin_x += self.options_len + OPTIONS_OFFSET

    def draw_option_selection_animation(self):
        selected_option = self.get_selected_option()
        begin_x = self.options_begin_x

        for index, option in enumerate(OPTIONS.keys()):
            if option != selected_option:
                begin_x += self.options_len + OPTIONS_OFFSET
                continue

            draw_message(self.options_begin_y, begin_x,
                         self.window, option, DEFAULT_COLOR)
            sleep(0.2)
            draw_message(self.options_begin_y, begin_x,
                         self.window, option, DEFAULT_COLOR + REVERSE)
            sleep(0.2)
            return

    def show_option_text(self, user_selection):
        self.window.clear()

        text = OPTIONS[user_selection]['text']
        y = (self.height - BASE_OFFSET) // 2
        x = (self.width // 2) - (len(text) // 2)

        draw_message(y, x, self.window, text)
        sleep(1)

    def redraw_window(self):
        self.setup_vars()
        self.initialize_settings()
