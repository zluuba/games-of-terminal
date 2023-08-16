from terminal_games.games.engine import GameEngine
from terminal_games.games.minesweeper.constants import *

import curses
import random

import time
import sys


class MinesweeperGame(GameEngine):
    def _setup(self):
        super()._setup()

        self.cell_width = 4
        self.cell_height = 2
        self.position = 0
        self.coords = (0, 0)
        self.bombs = []
        self.openCells = []

        self._draw_game_field()

        self._set_bombs()
        self._setup_side_menu()

    def _setup_side_menu(self):
        y, x = 1, 1

        for tip in SIDE_MENU_TIPS:
            self.side_menu_box.addstr(y, x, tip)
            y += 1

    def _get_game_box_size(self):
        height, width, *_ = self.sizes['game_box'].values()
        return width, height

    def _draw_game_field(self):
        width, height = self._get_game_box_size()

        begin_y, begin_x = curr_y, curr_x = 2, 1

        self.lines = height // self.cell_height
        self.cols = width // self.cell_width

        self.fields = {}
        curr_box_num = 0

        for _ in range(self.lines - 1):
            for _ in range(self.cols - 1):
                box = self.game_box.subwin(self.cell_height, self.cell_width, curr_y, curr_x)
                self.fields[curr_box_num] = box
                box.bkgd(curses.color_pair(4))

                curr_box_num += 1
                curr_x += self.cell_width

            curr_y += self.cell_height
            curr_x = begin_x

    def start_new_game(self):
        curses.curs_set(0)

        # self._draw_game_field()
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
        cols, rows = self.cols, self.lines

        self.game_field = [[j + i for j in range(rows + 1)] for i in range(0, (cols * (rows + 1)), (rows + 1))]

        row, col = self.coords
        new_row = r + row
        new_col = c + col

        if (0 <= new_row < rows - 1) and (0 <= new_col < cols - 1):
            self._update_field_color(curses.color_pair(4))

            self.coords = (new_row, new_col)
            self.position = self.game_field[new_row][new_col]
            self._update_field_color(curses.color_pair(5))

    def _update_field_color(self, color):
        field = self.fields[self.position]
        field.bkgd(' ', color)
        field.refresh()

    def _set_bombs(self):
        self.field_size = self.cols * self.lines
        num_of_bombs = self.field_size // 3

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
