from terminal_games.games.engine import GameEngine
from terminal_games.games.constants import KEYS
from terminal_games.games.minesweeper.constants import *
from terminal_games.games.minesweeper.common import Cell

import curses
from random import choice
import time


class MinesweeperGame(GameEngine):
    def _setup(self):
        super()._setup()

        self.cells = dict()

    def start_new_game(self):
        self._hide_cursor()
        self._draw_game_field()
        self._set_game_field()

        current_cell = self.cells[self.current_coordinates]
        current_cell.select()

        while True:
            key = self.window.getch()
            self._wait()

            if key == KEYS['escape']:
                curses.endwin()
                return

            if key in DIRECTIONS:
                offset = DIRECTIONS[key]
                self._slide_field(*offset)
            elif key == KEYS['q']:
                self._switch_flag()
            elif key in KEYS['enter']:
                current_cell = self.cells[self.current_coordinates]
                self._show_cell(current_cell)

            if self._is_all_cells_open():
                if self._is_no_unnecessary_flags():
                    self.game_status = 'game_over'
                    self._show_user_win()
                else:
                    self._show_user_have_unnecessary_flags()

            if self.game_status != 'game_is_on':
                curses.flash()

                self._draw_game_over_message()
                time.sleep(1)

                if self._is_restart():
                    self.__init__(self.canvas)
                    self.start_new_game()
                return

    def _set_game_field(self):
        self._plant_bombs()
        self._set_bombs_around_counter()
        self._open_first_empty_cell()

    def _draw_game_field(self):
        cell_height = 3
        cell_width = 7

        lines = (self.game_box_height - 2) // cell_height
        cols = (self.game_box_width - 2) // cell_width

        y = (self.game_box_height - (lines * cell_height)) // 2
        x = begin_x = (self.game_box_width - (cols * cell_width)) // 2

        y += self.sizes['game_box']['begin_y']
        x += self.sizes['game_box']['begin_x']

        self.current_coordinates = (y, x)

        for _ in range(lines):
            for _ in range(cols):
                field_box = self.game_box.subwin(cell_height, cell_width, y, x)
                field_box.bkgd(curses.color_pair(4))
                self.cells[(y, x)] = Cell(field_box, (y, x))

                x += cell_width

            y += cell_height
            x = begin_x

    def _slide_field(self, y_offset, x_offset):
        y, x = self.current_coordinates

        new_y = y + y_offset
        new_x = x + x_offset

        for cell_coordinates in self.cells.keys():
            if cell_coordinates == (new_y, new_x):
                # unselect current cell
                previous_cell = self.cells[self.current_coordinates]
                previous_cell.unselect()

                self.current_coordinates = (new_y, new_x)
                current_cell = self.cells[self.current_coordinates]
                current_cell.select()
                return

    def _plant_bombs(self):
        all_cells = list(self.cells.values())
        number_of_sells = len(all_cells)
        bombs_count = number_of_sells // 5

        while bombs_count != 0:
            cell = choice(all_cells)

            if not cell.is_bomb():
                cell.set_bomb()
                bombs_count -= 1

    def _set_bombs_around_counter(self):
        for coordinates, cell in self.cells.items():
            if cell.is_bomb():
                continue

            y, x = coordinates
            bombs = 0

            for y_offset, x_offset in CELL_OFFSETS:
                near_cell_coordinates = (y + y_offset, x + x_offset)

                if near_cell_coordinates in self.cells:
                    near_cell = self.cells[near_cell_coordinates]
                    bombs += 1 if near_cell.is_bomb() else 0

            cell.set_bombs_around_number(bombs)
            cell.set_background_color()

    def _open_first_empty_cell(self):
        empty_cells = self._get_empty_cells()

        if empty_cells:
            first_empty_cell = choice(empty_cells)
        else:
            first_empty_cell = choice(self.cells)

        first_empty_cell.open_cell()
        first_empty_cell.set_background_color()

    def _get_empty_cells(self):
        empty_cells = []

        for cell in self.cells.values():
            if self._is_cell_is_empty(cell):
                empty_cells.append(cell)

        return empty_cells

    @staticmethod
    def _is_cell_is_empty(cell):
        return not cell.is_bomb() and not cell.bombs_around()

    def _show_cell(self, cell):
        if cell.have_flag():
            return
        if not cell.is_open():
            # for first cell open we need to show cell color, not selected cell color
            cell.show_cell()
        if cell.is_bomb():
            cell.show_cell()
            self.game_status = 'game_over'

        cell.open_cell()
        cell.show_cell_text()
        cell.hide_cell()

    def _is_all_cells_open(self):
        for cell in self.cells.values():
            if not cell.is_open() and not cell.have_flag():
                return False
        return True

    def _is_no_unnecessary_flags(self):
        for cell in self.cells.values():
            if cell.have_flag() and not cell.is_bomb():
                return False
        return True

    def _switch_flag(self):
        cell = self.cells[self.current_coordinates]

        if cell.have_flag():
            cell.remove_flag()
        elif not cell.have_flag() and not cell.is_open():
            cell.set_flag()

        cell.show_cell()
        cell.show_cell_text()
        cell.hide_cell()

    def _show_user_win(self):
        self.side_menu_box.addstr(5, 1, 'You WIN!', curses.color_pair(9))
        self.side_menu_box.refresh()

    def _show_user_have_unnecessary_flags(self):
        self.side_menu_box.addstr(5, 1, 'The number of flags and bombs should match.', curses.color_pair(9))
        self.side_menu_box.refresh()

    # def _show_all_cells(self):
    #     for coords, cell in self.cells.items():
    #         self._show_cell(cell)

    # def _open_all_cells(self):
    #     for cell in self.cells.values():
    #         cell.open_cell()

    # def _open_near_empty_cells(self, cell):
    #     if cell.is_bomb:
    #         return
    #     if cell.bombs_around:
    #         cell.is_open = True
    #         cell.is_showed = True
    #         return
    #
    #     offsets = ((0, 7), (0, -7), (-3, 0), (3, 0))
    #     y, x = cell.coordinates
    #
    #     for offset_y, offset_x in offsets:
    #         near_cell_coordinates = (y + offset_y, x + offset_x)
    #
    #         if near_cell_coordinates in self.cells:
    #             near_cell = self.cells[near_cell_coordinates]
    #
    #             if self._is_cell_is_empty(near_cell) and not near_cell.is_open:
    #                 near_cell.is_open = True
    #                 near_cell.is_showed = True
    #                 cell.field_box.bkgd(' ', curses.color_pair(14))
    #                 cell.field_box.refresh()
    #                 self._open_near_empty_cells(near_cell)

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
