from games_of_terminal.constants import KEYS, DEFAULT_COLOR
from games_of_terminal.interface_manager import InterfaceManager
from games_of_terminal.log import log
from games_of_terminal.utils import (
    draw_message, hide_cursor, get_color_by_name,
)

from .constants import (
    TITLE, TITLE_OFFSET, ITEMS,
    NOISE_CHARS, NOISE_CHARS_LEN,
    NOISE_ANIMATION_DIV, NOISE_COLOR_NAME,
)

from curses import A_STANDOUT as REVERSE
from random import randint, choice


class Settings(InterfaceManager):
    @log
    def __init__(self, canvas, name):
        super().__init__(canvas, only_main_win=True)

        self.name = name

        self.items_len = len(ITEMS)
        self.current_row = 0

        self.setup_vars()

    @log
    def setup_vars(self):
        self.height, self.width = self.canvas.getmaxyx()

        self.title_start_y = self.get_title_start_y()
        self.items_start_y = self.get_items_start_y()

        self.chars_per_line = self.get_chars_per_line()
        self.noise_color = get_color_by_name(NOISE_COLOR_NAME)

    def get_title_start_y(self):
        return ((self.height // 2) -
                ((len(TITLE) + self.items_len) // 2) -
                TITLE_OFFSET)

    def get_items_start_y(self):
        return self.title_start_y + len(TITLE) + TITLE_OFFSET

    def get_chars_per_line(self):
        return self.width // NOISE_ANIMATION_DIV

    @log
    def run(self):
        self.initialize_settings()

        while True:
            key = self.window.getch()
            self.wait_for_keypress()

            if key == KEYS['escape']:
                return
            elif key == KEYS['resize']:
                self.window.timeout(0)
                self.resize_menu_win_handler(key)
            elif key in (KEYS['up_arrow'], KEYS['w']):
                self.move_menu_selection(-1)
            elif key in (KEYS['down_arrow'], KEYS['s']):
                self.move_menu_selection(1)
            elif key in KEYS['enter']:
                self.open_selected_settings()

            self.update_settings_display()
            self.window.refresh()

    @log
    def redraw_window(self):
        self.setup_vars()
        self.initialize_settings()

    @log
    def open_selected_settings(self):
        chosen_settings = ITEMS[self.current_row]
        settings_name = chosen_settings['name']
        settings_class = chosen_settings['class']

        settings = settings_class(self.canvas, settings_name)
        settings.run()

        self.handle_post_running_actions()

    @log
    def initialize_settings(self):
        hide_cursor()
        self.window.clear()

        self.update_settings_display()
        self.window.refresh()

    def update_settings_display(self):
        self.draw_noise_animation()
        self.show_settings_title()
        self.show_items_list()

    def show_settings_title(self):
        for y, line in enumerate(TITLE, start=self.title_start_y):
            x = (self.width // 2) - (len(line) // 2)
            draw_message(y, x, self.window, line)

    def show_items_list(self):
        begin_y = self.items_start_y

        for row, settings in enumerate(ITEMS.values()):
            settings_name = settings['name']

            begin_y += 1 if settings_name == 'Reset All' else 0
            y = begin_y + row
            x = (self.width // 2) - (len(settings_name) // 2)

            if row == self.current_row:
                color = DEFAULT_COLOR + REVERSE
            elif settings['status'] == 'in_development':
                color = get_color_by_name('grey_text_black_bg')
            else:
                color = DEFAULT_COLOR

            draw_message(y, x, self.window, settings_name, color)

    def move_menu_selection(self, direction):
        new_current_row = self.current_row + direction

        if new_current_row < 0:
            self.current_row = self.items_len - 1
        elif new_current_row >= self.items_len:
            self.current_row = 0
        else:
            self.current_row = new_current_row

    def draw_noise_animation(self):
        self.window.clear()

        curr_char_num = NOISE_CHARS_LEN
        start = self.height - 1
        end = self.height - 1 - NOISE_CHARS_LEN

        for _ in range(start, end, -1):
            for _ in range(self.chars_per_line):
                y = randint(0, self.height - 1)
                x = randint(0, self.width - 1)

                if not (1 < x < self.width - 1) or curr_char_num <= 0:
                    continue

                char = choice(NOISE_CHARS[:curr_char_num])
                self.window.addstr(y, x, char, self.noise_color)

            curr_char_num -= 1
