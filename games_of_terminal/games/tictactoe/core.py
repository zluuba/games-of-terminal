from games_of_terminal.constants import KEYS
from games_of_terminal.games.tictactoe.constants import (
    CELLS_IN_ROW, DIRECTIONS, WINNING_PATTERNS,
    BEST_MOVE_PATTERNS_BY_OWNERS, GAME_TIPS,
)
from games_of_terminal.games.engine import GameEngine
from games_of_terminal.games.tictactoe.cell import TicTacToeCell
from games_of_terminal.utils import hide_cursor

from random import choice
from time import sleep


class TicTacToeGame(GameEngine):
    def setup_game_stats(self):
        self.cells = {}
        self.current_coordinates = (0, 0)
        self.cell_height, self.cell_width = self._get_cell_size()

        self.user_moves = []
        self.computer_moves = []

    def setup_game_field(self, initial=True):
        hide_cursor()
        self.draw_logo()
        self.show_side_menu_tips(game_tips=GAME_TIPS)
        self.show_game_status()
        self._draw_game_field()

    def start_new_game(self):
        self.current_cell.select()

        while True:
            key = self.window.getch()
            self.wait_for_keypress()
            self.controller(key, pause_off=True)

            if self.stats.is_exit or self.stats.is_restart:
                return
            if self.is_game_over():
                # self._save_best_score()
                self.ask_for_restart()
                return

    def controller(self, key, pause_off=False):
        super().controller(key, pause_off)

        if key in DIRECTIONS:
            self._slide_field(key)
        elif key in KEYS['enter']:
            if self.current_cell.is_free():
                self._user_move()
                self._computer_move()

    @property
    def current_cell(self):
        return self.cells[self.current_coordinates]

    def _get_cell_size(self):
        """ Calculate cell sizes depending on the
        size of the game field.
        The ratio of cell width to cell height is always 2.5:1.
        """

        maximum_height = (self.game_area.height - 2) // CELLS_IN_ROW
        maximum_width = (self.game_area.width - 2) // CELLS_IN_ROW

        estimated_width = int(maximum_height * 2.5)
        estimated_height = int(maximum_width // 2.5)

        if estimated_width <= maximum_width:
            return maximum_height, estimated_width
        elif estimated_height <= maximum_height:
            return estimated_height, maximum_width

        while (estimated_height > maximum_height) \
                and (estimated_width > maximum_width):
            estimated_width -= 1
            estimated_height = int(estimated_width // 2.5)

        return estimated_height, estimated_width

    def _create_cell(self, y, x, cell_height, cell_width, field_number):
        field_box = self.game_area.box.subwin(cell_height, cell_width, y, x)
        cell = TicTacToeCell(field_box, (y, x))
        cell.field_number = field_number
        cell.set_background_color()
        return cell

    def _draw_game_field(self):
        y = (self.game_area.height - (CELLS_IN_ROW * self.cell_height)) // 2
        x = begin_x = (self.game_area.width - (CELLS_IN_ROW * self.cell_width)) // 2

        y += self.game_area.begin_y
        x += self.game_area.begin_x

        self.current_coordinates = (y, x)
        self.cells = {}
        field_number = 1

        for _ in range(CELLS_IN_ROW):
            for _ in range(CELLS_IN_ROW):
                cell = self._create_cell(y, x, self.cell_height, self.cell_width, field_number)
                self.cells[(y, x)] = cell

                x += self.cell_width
                field_number += 1

            y += self.cell_height
            x = begin_x

    def _slide_field(self, key):
        y, x = self.current_coordinates
        base_y_offset, base_x_offset = DIRECTIONS[key]

        y_offset = base_y_offset * self.cell_height
        x_offset = base_x_offset * self.cell_width

        new_coordinates = (y + y_offset, x + x_offset)

        if new_coordinates in self.cells.keys():
            self.current_cell.unselect()

            self.current_coordinates = new_coordinates
            self.current_cell.select()

    def _user_move(self):
        self.current_cell.owner = 'user'
        self.user_moves.append(self.current_cell.field_number)
        self._update_game_status()

    def _computer_move(self):
        if self.stats.game_status != 'game_active':
            return

        sleep(0.3)
        cell = self._get_best_move()
        cell.owner = 'computer'
        self.computer_moves.append(cell.field_number)
        self._update_game_status()

    def _get_best_move(self):
        cells_by_number = {cell.field_number: cell for cell in self.cells.values()}

        for best_move_pattern_by_owners in BEST_MOVE_PATTERNS_BY_OWNERS:
            for pattern in WINNING_PATTERNS:
                pattern_cells = [cells_by_number[num] for num in pattern]
                pattern_owners = [cell.owner for cell in pattern_cells]

                if sorted(pattern_owners) == sorted(best_move_pattern_by_owners):
                    best_move = [cell for cell in pattern_cells if cell.is_free()]
                    return best_move[0]

        random_move = self.get_random_empty_cell()
        return random_move

    def get_random_empty_cell(self):
        empty_cells = [cell for cell in self.cells.values() if cell.is_free()]
        random_cell = choice(empty_cells)

        return random_cell

    def _is_player_win(self, player):
        player_moves = self.user_moves if player == 'user' else self.computer_moves

        for winning_pattern in WINNING_PATTERNS:
            is_win = all(map(lambda cell_number: cell_number in player_moves, winning_pattern))
            if is_win:
                return True
        return False

    def _is_all_cells_occupied(self):
        for cell in self.cells.values():
            if cell.is_free():
                return False
        return True

    def _update_game_status(self):
        if self._is_player_win('user'):
            self.stats.game_status = 'user_win'
        elif self._is_player_win('computer'):
            self.stats.game_status = 'user_lose'
        elif self._is_all_cells_occupied():
            self.stats.game_status = 'tie'
