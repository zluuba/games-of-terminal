from terminal_games.scripts.tictactoe_game import start_tictactoe_game
from terminal_games.scripts.snake_game import start_snake_game
from terminal_games.games.constants import *

import curses
import random
import time
import sys


class Menu:
    def __init__(self, canvas):
        self.canvas = canvas

    def show_menu(self, stdscr, selected_row_ind):
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        for ind, item in enumerate(MENU):
            x = w // 2 - len(item) // 2
            y = h // 2 - len(MENU) // 2 + ind

            if ind == selected_row_ind:
                stdscr.addstr(y, x, item, curses.A_STANDOUT)
            else:
                stdscr.addstr(y, x, item)

        stdscr.refresh()

    def main(self):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

        h, w = self.canvas.getmaxyx()
        x = w // 2
        y = h // 2

        # set background
        self.canvas.bkgd(' ', curses.color_pair(1))

        menu_current_row_ind = 0
        self.show_menu(self.canvas, menu_current_row_ind)

        while True:
            key = self.canvas.getch()
            self.canvas.clear()

            # 27 - Esc button
            if key == 27:
                goodbye_message = random.choice(GOODBYE_WORDS)
                self.canvas.addstr(y, x - len(goodbye_message) // 2, goodbye_message)
                self.canvas.refresh()
                time.sleep(1.5)
                sys.exit(0)

            if key == curses.KEY_UP and menu_current_row_ind > 0:
                menu_current_row_ind -= 1
            elif key == curses.KEY_DOWN and menu_current_row_ind < len(MENU) - 1:
                menu_current_row_ind += 1
            elif key in (curses.KEY_ENTER, 10, 13):
                if menu_current_row_ind == 0:
                    start_snake_game(self.canvas)
                elif menu_current_row_ind == 1:
                    start_tictactoe_game(self.canvas)
                else:
                    self.canvas.addstr(
                        y, x - len(MENU[menu_current_row_ind]) // 2,
                        MENU[menu_current_row_ind]
                    )
                    self.canvas.refresh()
                    self.canvas.getch()

            self.show_menu(self.canvas, menu_current_row_ind)

            self.canvas.refresh()
