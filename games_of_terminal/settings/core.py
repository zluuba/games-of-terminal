from games_of_terminal.app_interface import InterfaceManager
from games_of_terminal.constants import KEYS

from .constants import TITLE, ITEMS, ITEMS_LEN

from curses import A_STANDOUT as REVERSE
from random import randint, choice


class Settings(InterfaceManager):
    def __init__(self, canvas, name):
        super().__init__(canvas)

        self.name = name
        self.current_row = 0

        self.title_start_y = (self.height // 2) - ((len(TITLE) + len(ITEMS)) // 2) - 3
        self.items_start_y = self.title_start_y + len(TITLE) + 3

    def run(self):
        self.initialize_settings()

        while True:
            key = self.window.getch()
            self.wait_for_keypress()

            if key == KEYS['escape']:
                return
            elif key in (KEYS['up_arrow'], KEYS['w']):
                self.move_menu_selection(-1)
            elif key in (KEYS['down_arrow'], KEYS['s']):
                self.move_menu_selection(1)

            self.update_menu_display()
            self.window.refresh()

    def initialize_settings(self):
        self.window.clear()
        self.hide_cursor()
        self.draw_noise_animation()
        self.draw_settings()

    def draw_settings(self):
        # draw static parts
        self.show_settings_title()
        self.show_items_list()
        self.window.refresh()

    def update_menu_display(self):
        # redraw dynamic parts
        self.draw_noise_animation()
        self.show_settings_title()
        self.show_items_list()

    def show_settings_title(self):
        for y, line in enumerate(TITLE, start=self.title_start_y):
            x = (self.width // 2) - (len(line) // 2)
            self.draw_message(y, x, self.window, line, self.default_color)

    def show_items_list(self):
        begin_y = self.items_start_y

        for row, game in enumerate(ITEMS.values()):
            game_name = game['name']

            begin_y += 1 if game_name == 'Reset All' else 0
            y = begin_y + row
            x = (self.width // 2) - (len(game_name) // 2)

            color = self.default_color + REVERSE if row == self.current_row \
                else self.default_color

            self.draw_message(y, x, self.window, game_name, color)

    def move_menu_selection(self, direction):
        self.current_row = max(
            0, min(self.current_row + direction, ITEMS_LEN - 1)
        )

    def draw_noise_animation(self):
        self.window.erase()

        chars = [' ', '.', '-', '-', '-', '|', '/', 'L']
        last_char_num = len(chars)

        for _ in range(self.height - 1, self.height - 1 - len(chars), -1):
            for _ in range(self.width // 3):
                y = randint(0, self.height - 1)
                x = randint(0, self.width - 1)
                color = self.get_color_by_name('grey_text_black_bg')
                char = choice(chars[:last_char_num]) if last_char_num > 0 else ' '

                if not (1 < x < self.width - 1):
                    continue

                self.window.addstr(y, x, char, color)
            last_char_num -= 1
