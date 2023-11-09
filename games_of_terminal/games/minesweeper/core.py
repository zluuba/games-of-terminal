from games_of_terminal.games.engine import GameEngine
from games_of_terminal.constants import KEYS
from games_of_terminal.games.minesweeper.constants import *
from games_of_terminal.games.minesweeper.cell import Cell

from curses import endwin, flash
from random import choice
from time import sleep


class MinesweeperGame(GameEngine):
    def _setup(self):
        super()._setup()

        self.cells = dict()
        self.flags = 0

    def start_new_game(self):
        self._setup_game_field()
        self.current_cell.select()

        while True:
            key = self.window.getch()
            self.wait_for_keypress()

            if key == KEYS['escape']:
                endwin()
                return

            if key in DIRECTIONS:
                offset = DIRECTIONS[key]
                self._slide_field(*offset)
            elif key == KEYS['q']:
                self._switch_flag()
            elif key in KEYS['enter']:
                self._show_cell(self.current_cell)

            self.draw_game_tips(self.tips)

            if self._is_all_cells_open():
                if self._is_no_unnecessary_flags():
                    self.game_status = 'user_win'

            if self.game_status != 'game_is_on':
                flash()

                self.show_game_status()
                sleep(1)

                if self._is_restart():
                    self.__init__(self.canvas)
                    self.start_new_game()
                return

    @property
    def current_cell(self):
        return self.cells[self.current_coordinates]

    @property
    def tips(self):
        return {'flags': self.flags}

    def _setup_game_field(self):
        self.hide_cursor()

        self._draw_game_field()
        self._plant_bombs()
        self._set_bombs_around_counter()
        self._open_first_empty_cell()

        self.show_game_status()
        self.setup_side_menu()
        self.draw_game_tips(self.tips)

    def _draw_game_field(self):
        lines = (self.game_area.height - GAME_FIELD_OFFSET_XY) // CELL_HEIGHT
        cols = (self.game_area.width - GAME_FIELD_OFFSET_XY) // CELL_WIDTH

        # initial coordinates of the upper left corner (centered)
        y = (self.game_area.height - (lines * CELL_HEIGHT)) // 2
        x = begin_x = (self.game_area.width - (cols * CELL_WIDTH)) // 2

        y += self.game_area.begin_y
        x += self.game_area.begin_x

        self.current_coordinates = (y, x)

        for _ in range(lines):
            for _ in range(cols):
                cell = self._create_cell(y, x)
                self.cells[(y, x)] = cell

                x += CELL_WIDTH

            y += CELL_HEIGHT
            x = begin_x

    def _create_cell(self, y, x):
        field_box = self.game_area.box.subwin(CELL_HEIGHT, CELL_WIDTH, y, x)
        cell = Cell(field_box, (y, x))
        cell.set_background_color()
        return cell

    def _slide_field(self, y_offset, x_offset):
        y, x = self.current_coordinates

        new_y = y + y_offset
        new_x = x + x_offset

        new_coordinates = (new_y, new_x)

        if new_coordinates in self.cells.keys():
            self.current_cell.unselect()

            self.current_coordinates = new_coordinates
            self.current_cell.select()

    def _plant_bombs(self):
        all_cells = list(self.cells.values())
        number_of_sells = len(all_cells)
        bombs_count = number_of_sells // 5
        self.flags = bombs_count

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
            if not cell.is_bomb() and not cell.bombs_around():
                empty_cells.append(cell)

        return empty_cells

    def _show_cell(self, cell):
        if cell.is_empty() and not cell.bombs_around():
            self._open_near_empty_cells(cell)

        if cell.have_flag():
            return
        if not cell.is_open():
            # for first cell open we need to show cell color,
            # not selected cell color
            cell.show_cell()
        if cell.is_bomb():
            cell.show_cell()
            self.game_status = 'user_lose'

        cell.open_cell()
        cell.show_cell_text()
        cell.hide_cell()

    def _open_near_empty_cells(self, cell):
        y, x = cell.coordinates

        for y_offset, x_offset in CELL_OFFSETS:
            new_y = y + y_offset
            new_x = x + x_offset

            near_cell_coordinates = (new_y, new_x)

            if near_cell_coordinates not in self.cells:
                continue

            near_cell = self.cells[near_cell_coordinates]

            if not near_cell.is_empty():
                continue

            near_cell.open_cell()
            near_cell.show_cell_text()

            if near_cell.bombs_around() > 0:
                continue

            self._open_near_empty_cells(near_cell)

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
        cell = self.current_cell

        if cell.have_flag():
            self.flags += 1
            cell.remove_flag()
        elif not cell.have_flag() and not cell.is_open() and self.flags > 0:
            self.flags -= 1
            cell.set_flag()

        cell.show_cell()
        cell.show_cell_text()
        cell.hide_cell()

    # def _show_all_cells(self):
    #     for coords, cell in self.cells.items():
    #         self._show_cell(cell)

    # def _open_all_cells(self):
    #     for cell in self.cells.values():
    #         cell.open_cell()

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
