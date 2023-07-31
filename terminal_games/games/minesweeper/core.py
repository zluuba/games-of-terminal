from terminal_games.games.engine import GameEngine
from terminal_games.games.minesweeper.constants import *

import curses
# import random

import time
import sys


class MinesweeperGame(GameEngine):
    def _setup(self):
        self.field_size = 5
        self.coords = (0, 0)
        self.position = 1

        super()._setup()

    def _draw_game_box(self):
        begin_y, begin_x = 1, 1
        end_y, end_x = 12, 22

        game_box = self.window.subwin(end_y, end_x, begin_y, begin_x)
        game_box.border()

    def _draw_game_field(self):
        self.fields = {}

        curr_box_num = 1
        lines, cols = 2, 4
        begin_y, begin_x = curr_y, curr_x = 2, 2

        for _ in range(self.field_size):
            for _ in range(self.field_size):
                box = self.window.subwin(lines, cols, curr_y, curr_x)
                self.fields[curr_box_num] = box
                box.bkgd(curses.color_pair(4))

                curr_box_num += 1
                curr_x += cols

            curr_y += lines
            curr_x = begin_x

    def start_new_game(self):
        curses.curs_set(0)

        self._draw_game_box()
        self._draw_game_field()

        self._update_field_color(curses.color_pair(2))

        while True:
            key = self.window.getch()
            self._wait()

            if key in DIRECTIONS:
                self._slide_field(*DIRECTIONS[key])
            elif key == 27:
                time.sleep(1)
                curses.endwin()
                sys.exit(0)

    def _slide_field(self, r, c):
        cols = rows = self.field_size
        row, col = self.coords
        new_row = r + row
        new_col = c + col

        if (0 <= new_row < rows) and (0 <= new_col < cols):
            self._update_field_color(curses.color_pair(4))

            self.coords = (new_row, new_col)
            self.position = FIELD[new_row][new_col]
            self._update_field_color(curses.color_pair(2))

    def _update_field_color(self, color):
        field = self.fields[self.position]
        field.bkgd(' ', color)
        field.refresh()


