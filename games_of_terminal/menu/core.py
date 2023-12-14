from games_of_terminal.app_interface import InterfaceManager
from games_of_terminal.constants import KEYS, BASE_OFFSET
from games_of_terminal.database.database import create_tables
from games_of_terminal.menu.constants import *

from curses import A_STANDOUT as REVERSE

from random import choice, random
from time import sleep
from sys import exit


class Menu(InterfaceManager):
    def _setup(self):
        super()._setup()

        # create tables in database
        create_tables()

        self.current_row = 0
        self.menu_length = len(GAMES)

        self.logo_start_y = (self.height // 2) - ((len(LOGO_MENU) + len(GAMES)) // 2) - 4
        self.menu_start_y = self.logo_start_y + len(LOGO_MENU) + 3

        self.top_sword_y = self.logo_start_y - 1
        self.top_sword_x = (self.width // 2) - (TOP_SWORD_LEN // 2)

        self.bottom_sword_y = self.logo_start_y + len(LOGO_MENU)
        self.bottom_sword_x = (self.width // 2) - (BOTTOM_SWORD_LEN // 2)

        self.fire_area_size = self.width * self.height
        self.fire_items = [0] * (self.fire_area_size + self.width + 1)

        end_offset = (BASE_OFFSET * 2) if (MENU_MAX_LEN % 2) else (BASE_OFFSET * 2 - 1)
        self.fire_free_area_begin_x = (self.width // 2) - (MENU_MAX_LEN // 2) - BASE_OFFSET
        self.fire_free_area_end_x = self.fire_free_area_begin_x + MENU_MAX_LEN + end_offset

        # self.logo_fill = choice(list(LOGO_FILL.values()))
        self.logo_fill = LOGO_FILL['default']

    def run_menu_loop(self):
        self.window.clear()
        self.hide_cursor()
        self._draw_menu()

        while True:
            key = self.window.getch()

            if key == KEYS['escape']:
                self._exit()
            if key == KEYS['resize']:
                self.redraw_window()

            if key in (KEYS['up_arrow'], KEYS['w']):
                self.current_row -= 1 if self.current_row > 0 else 0
            elif key in (KEYS['down_arrow'], KEYS['s']):
                is_end_of_menu = self.current_row >= self.menu_length - 1
                self.current_row += 1 if not is_end_of_menu else 0
            elif key in KEYS['enter']:
                chosen_game = GAMES[self.current_row]['game']
                new_game = chosen_game(self.canvas)
                new_game.start_new_game()
                self._draw_menu()

            self.window.refresh()
            self._fire_animation()

    def _draw_menu(self):
        self._draw_logo_with_swords()
        self._draw_creator_name()

    def _show_games_list(self):
        for row, game in enumerate(GAMES.values()):
            game_name = game['name']
            y = self.menu_start_y + row
            x = (self.width // 2) - (len(game_name) // 2)

            if row == self.current_row:
                self.draw_message(y, x, self.window,
                                  game_name, self.default_color + REVERSE)
            else:
                self.draw_message(y, x, self.window,
                                  game_name, self.default_color)

    def _draw_logo_with_swords(self):
        for y, line in enumerate(LOGO_MENU, start=self.logo_start_y):
            line = line.replace('#', self.logo_fill)
            x = (self.width // 2) - (len(line) // 2)
            self.draw_message(y, x, self.window, line, self.default_color)

        self._draw_sword(TOP_SWORD, self.top_sword_y, self.top_sword_x)
        self._draw_sword(BOTTOM_SWORD, self.bottom_sword_y, self.bottom_sword_x)

    def _draw_sword(self, sword, y, x):
        for name, part in sword:
            color = self.get_color_by_name(SWORD_COLORS[name])
            self.draw_message(y, x, self.window, part, color)
            x += len(part)

    def _draw_creator_name(self):
        color = self.get_color_by_name('light_grey_text_black_bg')
        begin_y = self.height - 2
        begin_x = (self.width // 2) - (len(CREATOR_NAME) // 2)

        self.draw_message(begin_y, begin_x, self.window,
                          CREATOR_NAME, color)

    def _draw_goodbye_message(self):
        goodbye_message = choice(GOODBYE_MESSAGES)
        begin_y = self.height // 2
        begin_x = (self.width // 2) - (len(goodbye_message) // 2)

        self.draw_message(begin_y, begin_x, self.window,
                          goodbye_message, self.default_color)
        self.window.refresh()

    def _exit(self):
        self.window.clear()
        self._draw_goodbye_message()
        sleep(1)
        exit(0)

    def _fire_animation(self, animation=True, empty_middle=True):
        if not animation:
            return

        self.window.timeout(ANIMATION_SPEED['medium'])

        for i in range(int(self.width / 9)):
            self.fire_items[int((random() * self.width) + self.width * (self.height - 1))] = FIRE_ELEMENTS_COUNT

        for i in range(self.fire_area_size):
            self.fire_items[i] = int(
                (self.fire_items[i] + self.fire_items[i + 1] + self.fire_items[i + self.width] +
                 + self.fire_items[i + self.width + 1]) / 4
            )
            color_name = ('yellow' if self.fire_items[i] > 15 else ('red' if self.fire_items[i] > 9 else 'black'))
            color = self.get_color_by_name(FIRE_COLORS[color_name])

            fire_char_index = LAST_FIRE_CHAR_IND if self.fire_items[i] > LAST_FIRE_CHAR_IND else self.fire_items[i]
            char = FIRE_CHARS[fire_char_index]

            y = int(i / self.width)
            x = int(i % self.width)

            if i >= self.fire_area_size - 1:
                continue

            if empty_middle and (self.fire_free_area_begin_x <= x <= self.fire_free_area_end_x):
                continue

            self.window.addstr(y, x, char, color)

        self._show_games_list()
        self.window.refresh()
