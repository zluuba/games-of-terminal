from terminal_games.games.constants import KEYS
from terminal_games.games.tictactoe.constants import *
from terminal_games.games.engine import GameEngine

import curses
import random
import time


class TicTacToeGame(GameEngine):
    def _setup(self):
        super()._setup()

        self.position = 5
        self.coords = (1, 1)

        self.moves = []
        self.user_moves = []
        self.computer_moves = []

        self.game_status = 'game_is_on'

    def _draw_game_field(self):
        self.fields = {}

        curr_box_num = 1
        lines, cols = 5, 10

        middle_y = (self.game_box_height // 2) - (lines // 2)
        middle_x = (self.game_box_width // 2) - (cols // 2)

        begin_ys = (middle_y - 4, middle_y, middle_y + 4)
        begin_xs = (middle_x - 9, middle_x, middle_x + 9)

        for begin_y in begin_ys:
            for begin_x in begin_xs:
                box = self.game_box.subwin(lines, cols, begin_y, begin_x)
                box.border()
                self.fields[curr_box_num] = box

                curr_box_num += 1

    def start_new_game(self):
        curses.curs_set(0)

        self._draw_game_field()
        self._fill_field(self.fields[self.position], curses.color_pair(2))

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
                is_move_taken = self._user_move()
                if is_move_taken and self.game_status == 'game_is_on':
                    time.sleep(0.5)
                    self._computer_move()

            if self.game_status != 'game_is_on':
                curses.flash()

                self._draw_game_over_message()
                time.sleep(1)

                if self._is_restart():
                    self.__init__(self.canvas)
                    self.start_new_game()
                return

    def _user_move(self):
        if self.position not in self.moves:
            self.moves.append(self.position)
            self.user_moves.append(self.position)
            self._fill_field(self.fields[self.position], curses.color_pair(12))
            self._set_game_status()
            return True
        return False

    def _computer_move(self):
        chosen_field = None

        while chosen_field is None:
            move = random.randint(1, 9)
            if move not in self.moves:
                move = self._get_best_move(move)
                self.moves.append(move)
                self.computer_moves.append(move)
                chosen_field = move

        self._fill_field(self.fields[chosen_field], curses.color_pair(13))
        self._set_game_status()

    def _get_best_move(self, curr_move):
        for x, y, z in WINNING_COMBINATIONS:
            if x in self.computer_moves and y in self.computer_moves and z not in self.moves:
                return z
            if x in self.computer_moves and z in self.computer_moves and y not in self.moves:
                return y
            if y in self.computer_moves and z in self.computer_moves and x not in self.moves:
                return x

        for x, y, z in WINNING_COMBINATIONS:
            if x in self.user_moves and y in self.user_moves and z not in self.moves:
                return z
            if x in self.user_moves and z in self.user_moves and y not in self.moves:
                return y
            if y in self.user_moves and z in self.user_moves and x not in self.moves:
                return x

        return curr_move

    def _check_to_win(self, player):
        player_moves = self.user_moves if player == 'user' else self.computer_moves
        for winning_moves in WINNING_COMBINATIONS:
            is_win = all(map(lambda move: move in player_moves, winning_moves))
            if is_win:
                return True
        return False

    def _set_game_status(self):
        if self._check_to_win('user'):
            self.game_status = 'user_win'
        elif self._check_to_win('computer'):
            self.game_status = 'computer_win'
        elif len(self.moves) == 9:
            self.game_status = 'tie'
        else:
            self.game_status = 'game_is_on'

    def _slide_field(self, r, c):
        cols, rows = 3, 3
        row, col = self.coords
        new_row = r + row
        new_col = c + col

        if (0 <= new_row < rows) and (0 <= new_col < cols):
            self.coords = (new_row, new_col)
            self._reset_field_color(self.position)

            self.position = FIELD[new_row][new_col]
            self._fill_field(self.fields[self.position], curses.color_pair(2))

    @staticmethod
    def _fill_field(field, color):
        h, w = field.getmaxyx()

        for y in range(1, h - 1):
            for x in range(1, w - 1):
                field.addstr(y, x, ' ', color)

        field.refresh()

    def _reset_field_color(self, position):
        if position in self.user_moves:
            color = curses.color_pair(12)
        elif position in self.computer_moves:
            color = curses.color_pair(13)
        else:
            color = curses.color_pair(1)

        field = self.fields[self.position]
        self._fill_field(field, color)
