from terminal_games.games.engine import GameEngine
from terminal_games.games.minesweeper.constants import *

import curses
import random

import time
import sys


class MinesweeperGame(GameEngine):
    def _setup(self):
        super()._setup()

        self.field_size = 5
        self.position = 1
        self.coords = (0, 0)
        self.bombs = []
        self.openCells = []

        self._set_bombs()
        self._setup_side_menu()

    def _setup_side_menu(self):
        y, x = 1, 1

        for tip in SIDE_MENU_TIPS:
            self.side_menu_box.addstr(y, x, tip)
            y += 1

    def _draw_box(self):
        begin_y, begin_x = 2, 2
        end_y, end_x = 17, 32

        game_box = self.window.subwin(end_y, end_x, begin_y, begin_x)
        game_box.border()

    def _draw_game_field(self):
        self.fields = {}

        curr_box_num = 1
        lines, cols = 3, 6
        begin_y, begin_x = curr_y, curr_x = 3, 3

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

        self._draw_box()
        self._draw_game_field()
        self._update_field_color(curses.color_pair(5))

        while True:
            key = self.window.getch()
            self._wait()

            if key in DIRECTIONS:
                self._slide_field(*DIRECTIONS[key])
            elif key in (curses.KEY_ENTER, 10, 13):
                self._show_field()
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
            self._update_field_color(curses.color_pair(5))

    def _update_field_color(self, color):
        field = self.fields[self.position]
        field.bkgd(' ', color)
        field.refresh()

    def _set_bombs(self):
        num_of_bombs = self.field_size ** 2 // 3

        while num_of_bombs > 0:
            bomb_field = random.randint(1, self.field_size ** 2)

            if bomb_field not in self.bombs:
                self.bombs.append(bomb_field)
                num_of_bombs -= 1

    def _show_field(self):
        field = self.fields[self.position]

        if self.position in self.openCells:
            return
        elif self.position in self.bombs:
            field.addstr('*', curses.color_pair(3))
        else:
            field.addstr('-', curses.color_pair(2))

        field.refresh()
        self.openCells.append(self.position)
