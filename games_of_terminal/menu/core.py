from games_of_terminal.app_interface import InterfaceManager
from games_of_terminal.constants import KEYS
from games_of_terminal.menu.constants import (
    GAMES, CREATOR_NAME, GOODBYE_MESSAGES
)

from curses import A_STANDOUT as REVERSE_COLORS

from random import choice
from time import sleep
from sys import exit


class Menu(InterfaceManager):
    def _setup(self):
        super()._setup()

        self.current_row = 0
        self.menu_length = len(GAMES)

    def run_menu_loop(self):
        self.hide_cursor()

        while True:
            key = self.window.getch()
            self.wait_for_keypress()

            if key == KEYS['escape']:
                self._exit()
            elif key == KEYS['up_arrow']:
                self.current_row -= 1 if self.current_row > 0 else 0
            elif key == KEYS['down_arrow']:
                is_end_of_menu = self.current_row >= self.menu_length - 1
                self.current_row += 1 if not is_end_of_menu else 0
            elif key in KEYS['enter']:
                chosen_game = GAMES[self.current_row]['game']
                new_game = chosen_game(self.canvas)
                new_game.start_new_game()

            self._show_menu()
            self.window.refresh()

    def _show_menu(self):
        self.window.clear()

        for row, game in enumerate(GAMES.values()):
            game_name = game['name']
            x = (self.width // 2) - (len(game_name) // 2)
            y = (self.height // 2) - (self.menu_length // 2) + row

            if row == self.current_row:
                self.draw_message(y, x, self.window, game_name,
                                  self.default_color + REVERSE_COLORS)
            else:
                self.draw_message(y, x, self.window, game_name,
                                  self.default_color)

        self._draw_creator_name()

    def _draw_creator_name(self):
        color = self.get_color_by_name('dark_grey_text_black_bg')
        y = self.height - 2
        x = (self.width // 2) - (len(CREATOR_NAME) // 2)

        self.draw_message(y, x, self.window, CREATOR_NAME, color)

    def _exit(self):
        self.window.clear()
        self._draw_goodbye_message()
        sleep(1)
        exit(0)

    def _draw_goodbye_message(self):
        goodbye_message = choice(GOODBYE_MESSAGES)
        begin_y = self.height // 2
        begin_x = (self.width // 2) - (len(goodbye_message) // 2)

        self.draw_message(begin_y, begin_x, self.window,
                          goodbye_message, self.default_color)
