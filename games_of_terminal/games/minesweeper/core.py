from games_of_terminal.constants import KEYS, BASE_OFFSET
from games_of_terminal.database.database import update_game_stat
from games_of_terminal.games.engine import GameEngine
from games_of_terminal.games.minesweeper.achievements_manager import (
    MinesweeperAchievementsManager,
)
from games_of_terminal.games.minesweeper.constants import (
    CELL_HEIGHT, CELL_WIDTH, CELL_OFFSETS,
    GAME_TIPS, DIRECTIONS,
)
from games_of_terminal.games.minesweeper.cell import Cell
from games_of_terminal.utils import (
    hide_cursor,
    update_total_time_count,
    update_total_games_count,
)

from random import choice, uniform
from time import time


class MinesweeperGame(GameEngine):
    def setup_game_stats(self):
        self.start_time = time()

        self.cells = dict()
        self.flags = 0
        self.bombs = 0

        self.current_coordinates = self.get_begin_coordinates()
        self.achievement_manager = MinesweeperAchievementsManager(self)

    def get_lines_and_columns_count(self):
        lines = (self.game_area.height - BASE_OFFSET) // CELL_HEIGHT
        columns = (self.game_area.width - BASE_OFFSET) // CELL_WIDTH

        return lines, columns

    def get_begin_coordinates(self):
        lines, columns = self.get_lines_and_columns_count()

        y = (self.game_area.height - (lines * CELL_HEIGHT)) // 2
        x = (self.game_area.width - (columns * CELL_WIDTH)) // 2

        y += self.game_area.begin_y
        x += self.game_area.begin_x

        return y, x

    def setup_game_field(self):
        hide_cursor()

        self.draw_game_field(initial=True)
        self.plant_bombs()
        self.set_bombs_around_counter()
        self.open_first_empty_cell()

        self.draw_side_menu_logo()
        self.show_side_menu_tips(
            game_state=self.tips,
            game_tips=GAME_TIPS,
        )
        self.show_game_status()

    def start_new_game(self):
        self.current_cell.select()

        while True:
            key = self.window.getch()
            self.wait_for_keypress()
            self.controller(key, pause_on=False)

            if self.stats.is_exit or self.stats.is_restart:
                self.save_game_data(is_game_over=False)
                self.achievement_manager.check()
                return
            if self.is_game_over():
                self.save_game_data()
                self.achievement_manager.check()
                self.ask_for_restart()
                return

    def controller(self, key, pause_on=True):
        super().controller(key, pause_on)

        if key in DIRECTIONS:
            offset = DIRECTIONS[key]
            self.slide_field(*offset)
        elif key == KEYS['q']:
            self.switch_flag()
        elif key in KEYS['enter']:
            self.show_cell(self.current_cell)

    @property
    def current_cell(self):
        return self.cells[self.current_coordinates]

    @property
    def tips(self):
        return {'flags': self.flags}

    def draw_game_field(self, initial=False, change_color_scheme=False):
        lines, columns = self.get_lines_and_columns_count()
        y, x = self.get_begin_coordinates()
        begin_x = x

        for _ in range(lines):
            for _ in range(columns):
                if initial:
                    cell = self.create_cell(y, x)
                    self.cells[(y, x)] = cell
                else:
                    if change_color_scheme:
                        self.cells[(y, x)].set_color_scheme()

                    self.cells[(y, x)].clear_cell()
                    self.cells[(y, x)].update_cell_color()
                    self.cells[(y, x)].show_cell_text()

                x += CELL_WIDTH

            y += CELL_HEIGHT
            x = begin_x

    def create_cell(self, y, x):
        field_box = self.game_area.box.subwin(CELL_HEIGHT, CELL_WIDTH, y, x)
        cell = Cell(field_box, (y, x), self.game_name)
        cell.set_background_color()
        return cell

    def slide_field(self, y_offset, x_offset):
        y, x = self.current_coordinates

        new_y = y + y_offset
        new_x = x + x_offset

        new_coordinates = (new_y, new_x)

        if new_coordinates in self.cells.keys():
            self.current_cell.unselect()

            self.current_coordinates = new_coordinates
            self.current_cell.select()

    def plant_bombs(self):
        all_cells = list(self.cells.values())
        number_of_sells = len(all_cells)

        div = uniform(3, 8)
        bombs_count = number_of_sells // div
        self.bombs = int(bombs_count)
        self.flags = self.bombs

        while bombs_count != 0:
            cell = choice(all_cells)

            if not cell.is_bomb():
                cell.set_bomb()
                bombs_count -= 1

    def set_bombs_around_counter(self):
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

            cell.bombs_around = bombs
            cell.set_background_color()

    def open_first_empty_cell(self):
        empty_cells = self.get_empty_cells()

        if not empty_cells:
            self.setup_game_field()
            return

        first_empty_cell = choice(empty_cells)
        first_empty_cell.open_cell()
        first_empty_cell.set_background_color()

    def get_empty_cells(self):
        empty_cells = []

        for cell in self.cells.values():
            if not cell.is_bomb() and not cell.bombs_around:
                empty_cells.append(cell)

        return empty_cells

    def show_cell(self, cell):
        if cell.have_flag():
            return

        if cell.is_empty() and not cell.bombs_around:
            self.open_near_empty_cells(cell)
        if not cell.is_open():
            cell.show_cell()
        if cell.is_bomb():
            self.stats.game_status = 'user_lose'

        cell.open_cell()
        cell.show_cell_text()
        cell.hide_cell()
        self.check_to_win()

    def switch_flag(self):
        if self.current_cell.is_open():
            return
        if not self.flags and not self.current_cell.have_flag():
            self.achievement_manager.check(extra_flag=True)
            return

        if self.current_cell.have_flag():
            self.flags += 1
            self.current_cell.remove_flag()
        elif (not self.current_cell.have_flag() and
              not self.current_cell.is_open()):
            self.flags -= 1
            self.current_cell.set_flag()

        self.current_cell.show_cell()
        self.current_cell.show_cell_text()
        self.current_cell.hide_cell()

        self.show_side_menu_tips(
            game_state=self.tips,
            game_tips=GAME_TIPS,
        )
        self.check_to_win()

    def open_near_empty_cells(self, cell):
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

            if near_cell.bombs_around > 0:
                continue

            self.open_near_empty_cells(near_cell)

    def is_all_cells_open(self):
        for cell in self.cells.values():
            if not cell.is_open() and not cell.have_flag():
                return False
        return True

    def is_no_unnecessary_flags(self):
        for cell in self.cells.values():
            if cell.have_flag() and not cell.is_bomb():
                return False
        return True

    def check_to_win(self):
        if self.is_all_cells_open() and self.is_no_unnecessary_flags():
            self.stats.game_status = 'user_win'

    def save_game_data(self, is_game_over=True):
        update_total_time_count(self.game_name, self.start_time)

        if is_game_over:
            update_total_games_count(self.game_name, 1)
            self.update_bombs_defused_count()
            self.update_end_game_status_stat()

    def update_end_game_status_stat(self):
        if self.stats.game_status == 'user_win':
            end_game_status_stat_name = 'total_wins'
        else:
            end_game_status_stat_name = 'total_losses'

        update_game_stat(self.game_name, end_game_status_stat_name, 1)

    def update_bombs_defused_count(self):
        bombs_defused = sum([
            1 for cell in self.cells.values()
            if (cell.is_bomb() and cell.have_flag())
        ])
        update_game_stat(self.game_name, 'bombs_defused', bombs_defused)

    def draw_game_window(self):
        self.draw_basic_window_view()
        self.show_side_menu_tips(
            game_state=self.tips,
            game_tips=GAME_TIPS,
        )

        self.current_cell.unselect()
        self.draw_game_field(change_color_scheme=True)
        self.current_cell.select()

        self.check_achievements()

    def check_achievements(self):
        if self.is_settings_option_was_change('color_schemes'):
            self.achievement_manager.check(color_scheme_change=True)
