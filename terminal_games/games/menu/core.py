from terminal_games.games.menu.constants import *

import curses
import random
import time
import sys


class Menu:
    def __init__(self, canvas):
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
        self._change_the_game()
        self._show_menu()

        while True:
            key = self.canvas.getch()
            self.canvas.clear()

            # 27 - Esc button
            if key == 27:
                self._exit()
            elif key == curses.KEY_UP and self.curr_row > 1:
                self.curr_row -= 1
            elif key == curses.KEY_DOWN and self.curr_row < self.menu_length:
                self.curr_row += 1
            elif key in (curses.KEY_ENTER, 10, 13):
                self.game.start_new_game()

            self._change_the_game()
            self._show_menu()
            self.canvas.refresh()

    def _change_the_game(self):
        current_game = GAMES[self.curr_row]['game']
        self.game = current_game(self.canvas)

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
