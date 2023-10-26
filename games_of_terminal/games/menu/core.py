from games_of_terminal.games.menu.constants import GAMES, GOODBYE_MESSAGES
from games_of_terminal.games.constants import KEYS
from games_of_terminal.games.engine import Engine

from random import choice
import curses
import time
import sys


class Menu(Engine):
    def _setup(self):
        super()._setup()

        self.curr_row = 1
        self.menu_length = len(GAMES)

    def _show_menu(self):
        color = self.get_color_by_name('white_text_black_bg')
        reversed_color = color + curses.A_STANDOUT
        self.window.clear()

        for row, item in enumerate(GAMES.values(), start=1):
            game_name = item['name']
            x = self.width // 2 - len(game_name) // 2
            y = self.height // 2 - self.menu_length // 2 + row

            if row == self.curr_row:
                self.window.addstr(y, x, game_name, reversed_color)
            else:
                self.window.addstr(y, x, game_name, color)

        self.window.refresh()

    def main(self):
        curses.curs_set(0)
        self._show_menu()

        while True:
            key = self.window.getch()

            if key == KEYS['escape']:
                self._exit()
            elif key == KEYS['up_arrow'] and self.curr_row > 1:
                self.curr_row -= 1
            elif key == KEYS['down_arrow'] and self.curr_row < self.menu_length:
                self.curr_row += 1
            elif key in KEYS['enter']:
                chosen_game = GAMES[self.curr_row]['game']
                new_game = chosen_game(self.window)
                new_game.start_new_game()

            self._show_menu()
            self.window.refresh()

    def _exit(self):
        self.window.clear()

        goodbye_message = choice(GOODBYE_MESSAGES)
        self.window.addstr(
            self.height // 2,
            (self.width // 2) - len(goodbye_message) // 2,
            goodbye_message,
            self.get_color_by_name('white_text_black_bg'),
        )
        self.window.refresh()

        time.sleep(1)
        sys.exit(0)
