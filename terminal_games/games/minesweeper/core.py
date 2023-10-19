from terminal_games.games.engine import GameEngine
from terminal_games.games.constants import KEYS
from terminal_games.games.minesweeper.constants import *

import curses
from random import choice
import time


class Cell:
    def __init__(self, field_box):
        self.field_box = field_box

        self.is_open = False
        self.is_bomb = False
        self.bombs_around = 0


class MinesweeperGame(GameEngine):
    def _setup(self):
        super()._setup()

        self.cells = dict()
        self.coordinates = (2, 2)

    def start_new_game(self):
        curses.curs_set(0)

        self._draw_game_field()
        self._plant_bombs()
        self._update_field_color(curses.color_pair(5))

        while True:
            key = self.window.getch()
            self._wait()

            if key == KEYS['escape']:
                curses.endwin()
                return

            if key in DIRECTIONS:
                offset = DIRECTIONS[key]
                self._slide_field(*offset)
            elif key in KEYS['enter']:
                current_cell = self.cells[self.coordinates]
                self._show_cell(current_cell)
                # self._open_all_cells()
                # self._show_all_cells()
                # self._update_current_field_color()
                pass

    def _draw_game_field(self):
        cell_height = 3
        cell_width = 7

        lines = (self.game_box_height - 2) // cell_height
        cols = (self.game_box_width - 2) // cell_width

        y = (self.game_box_height - (lines * cell_height)) // 2
        x = begin_x = (self.game_box_width - (cols * cell_width)) // 2

        y += self.sizes['game_box']['begin_y']
        x += self.sizes['game_box']['begin_x']

        for _ in range(lines):
            for _ in range(cols):
                field_box = self.game_box.subwin(cell_height, cell_width, y, x)
                field_box.bkgd(curses.color_pair(4))
                self.cells[(y, x)] = Cell(field_box)

                x += cell_width

            y += cell_height
            x = begin_x

    def _slide_field(self, r, c):
        y, x = self.coordinates

        new_y = y + r
        new_x = x + c

        for field_coordinates in self.cells.keys():
            if field_coordinates == (new_y, new_x):
                self._update_field_color(curses.color_pair(4))

                self.coordinates = (new_y, new_x)
                self._update_current_field_color()
                return

    def _plant_bombs(self):
        cells_count = len(self.cells.keys())
        bombs_count = cells_count // 5

        while bombs_count != 0:
            cell = choice(list(self.cells.values()))

            if not cell.is_bomb:
                cell.is_bomb = True
                bombs_count -= 1

    def _update_current_field_color(self):
        cell = self.cells[self.coordinates]
        cell.field_box.bkgd(' ', curses.color_pair(5))
        cell.field_box.refresh()

    def _update_field_color(self, color):
        cell = self.cells[self.coordinates]

        if cell.is_open:
            self._show_cell(cell)
        else:
            cell.field_box.bkgd(' ', color)
            cell.field_box.refresh()

    @staticmethod
    def _show_cell(cell):
        cell.is_open = True

        center_y = 3
        center_x = 1

        cell.field_box.bkgd(' ', curses.color_pair(1))

        if cell.is_bomb:
            cell.field_box.addstr(
                center_x, center_y,
                '*',
                curses.color_pair(11),
            )
        elif cell.bombs_around > 0:
            cell.field_box.addstr(
                center_x, center_y,
                str(cell.bombs_around),
                curses.color_pair(10),
            )

        cell.field_box.refresh()

    def _show_all_cells(self):
        for coords, cell in self.cells.items():
            self._show_cell(cell)

    def _open_all_cells(self):
        for cell in self.cells.values():
            cell.is_open = True

    # def _check_window_resize(self):
    #     self.resize = curses.is_term_resized(self.height, self.width)
    #
    #     if self.resize is True:
    #         curses.flash()
    #         self.canvas.clear()
    #         y, x = self.canvas.getmaxyx()
    #         curses.resizeterm(y, x)
    #         self.height, self.width = y, x
    #         self.canvas.refresh()
    #         self._setup()
