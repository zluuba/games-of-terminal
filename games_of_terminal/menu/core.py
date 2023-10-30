from games_of_terminal.app_interface import InterfaceManager
from games_of_terminal.constants import KEYS
from games_of_terminal.menu.constants import GAMES, GOODBYE_MESSAGES

from random import choice
import curses
import time
import sys


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
                self.current_row += 1 if self.current_row < self.menu_length - 1 else 0
            elif key in KEYS['enter']:
                chosen_game = GAMES[self.current_row]['game']
                new_game = chosen_game(self.canvas)
                new_game.start_new_game()

            self._show_menu()
            self.window.refresh()

    def _show_menu(self):
        self.window.clear()

        for row, item in enumerate(GAMES.values()):
            game_name = item['name']
            x = self.width // 2 - len(game_name) // 2
            y = self.height // 2 - self.menu_length // 2 + row

            if row == self.current_row:
                self.window.addstr(y, x, game_name, self.default_color + curses.A_STANDOUT)
            else:
                self.window.addstr(y, x, game_name, self.default_color)

        self.window.refresh()

    def _exit(self):
        self.window.clear()
        self._draw_goodbye_message()
        time.sleep(1)
        sys.exit(0)

    def _draw_goodbye_message(self):
        goodbye_message = choice(GOODBYE_MESSAGES)

        begin_y = self.height // 2
        begin_x = (self.width // 2) - len(goodbye_message) // 2

        self.draw_message(begin_y, begin_x, self.window, goodbye_message, self.default_color)