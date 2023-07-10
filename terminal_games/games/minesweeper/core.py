import curses
import random

import time
import sys


DIRECTIONS = {
    curses.KEY_RIGHT: (0, 1), curses.KEY_LEFT: (0, -1),
    curses.KEY_UP: (-1, 0), curses.KEY_DOWN: (1, 0),
}
FIELD = [[1, 2, 3, 4, 5],
         [6, 7, 8, 9, 10],
         [11, 12, 13, 14, 15],
         [16, 17, 18, 19, 20],
         [21, 22, 23, 24, 25]]


class MinesweeperGame:
    def __init__(self, canvas):
        self.canvas = canvas
        self._setup()

    def _setup(self):
        self._init_colors()
        self.height, self.width = self.canvas.getmaxyx()
        self._setup_game_window()

        self.canvas.bkgd(' ', curses.color_pair(1))
        self.field_size = 5

        self.position = 1
        self.coords = (0, 0)

    def _init_colors(self):
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)

    def _setup_game_window(self):
        self.window = curses.newwin(self.height - 2, self.width - 2, 1, 1)
        self.window.nodelay(True)
        self.window.keypad(True)
        self.window.border()

    def _draw_game_field(self):
        self.fields = {}

        curr_box_num = 1
        lines, cols = 2, 4
        begin_y, begin_x = curr_y, curr_x = 2, 2

        for _ in range(self.field_size):
            for _ in range(self.field_size):
                box = self.window.subwin(lines, cols, curr_y, curr_x)
                self.fields[curr_box_num] = box
                box.border()

                curr_box_num += 1
                curr_x += cols

            curr_y += lines
            curr_x = begin_x

    def start_new_game(self):
        curses.curs_set(0)

        self._draw_game_field()
        self._update_field_color()

        while True:
            key = self.window.getch()

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
            self.coords = (new_row, new_col)
            self.position = FIELD[new_row][new_col]
            self._reset_fields_color()
            self._update_field_color()

    def _reset_fields_color(self):
        for pos, field in self.fields.items():
            field.bkgd(' ', curses.color_pair(1))
            field.refresh()

    def _update_field_color(self):
        window = self.fields[self.position]
        window.bkgd(' ', curses.color_pair(2))
        window.refresh()


