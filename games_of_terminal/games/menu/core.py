from games_of_terminal.games.menu.constants import *
from games_of_terminal.games.constants import KEYS

import curses
import random
import time
import sys


class Menu:
    def __init__(self, canvas):
        # TODO:
        #  - draw window instead of raw canvas
        #  - do I need to use GameEngine class there? For initial setup

        self.canvas = canvas
        self._setup()

    def _setup(self):
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

        self.canvas.bkgd(' ', curses.color_pair(1))
        self.height, self.width = self.canvas.getmaxyx()

        self.curr_row = 1
        self.menu_length = len(GAMES)

    def _show_menu(self):
        self.canvas.clear()

        for row, item in enumerate(GAMES.values(), start=1):
            game_name = item['name']
            x = self.width // 2 - len(game_name) // 2
            y = self.height // 2 - self.menu_length // 2 + row

            if row == self.curr_row:
                self.canvas.addstr(y, x, game_name, curses.A_STANDOUT)
            else:
                self.canvas.addstr(y, x, game_name)

        self.canvas.refresh()

    def main(self):
        curses.curs_set(0)
        self._show_menu()

        while True:
            key = self.canvas.getch()
            self.canvas.clear()

            if key == KEYS['escape']:
                self._exit()
            elif key == KEYS['up_arrow'] and self.curr_row > 1:
                self.curr_row -= 1
            elif key == KEYS['down_arrow'] and self.curr_row < self.menu_length:
                self.curr_row += 1
            elif key in KEYS['enter']:
                chosen_game = GAMES[self.curr_row]['game']
                new_game = chosen_game(self.canvas)
                new_game.start_new_game()

            self._show_menu()
            self.canvas.refresh()

    def _exit(self):
        goodbye_message = random.choice(GOODBYE_MESSAGES)
        self.canvas.addstr(
            self.height // 2,
            (self.width // 2) - len(goodbye_message) // 2,
            goodbye_message,
        )
        self.canvas.refresh()

        time.sleep(1)
        sys.exit(0)
