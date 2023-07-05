import curses
import random
import sys
import time


# TODO: add double win (two winning combinations in one game)


DIRECTIONS = {
    curses.KEY_RIGHT: (0, 1), curses.KEY_LEFT: (0, -1),
    curses.KEY_UP: (-1, 0), curses.KEY_DOWN: (1, 0),
}
FIELD = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]

WINNING_COMBINATIONS = ((1, 2, 3), (4, 5, 6), (7, 8, 9),
                        (1, 4, 7), (2, 5, 8), (3, 6, 9),
                        (1, 5, 9), (3, 5, 7))

GAME_STATUSES = {
    0: 'User win!',
    1: 'Computer win!',
    2: 'Tie!',
}


class TicTacToeGame:
    def __init__(self, canvas):
        self.canvas = canvas
        self._setup()

    def _setup(self):
        self._init_colors()
        self.height, self.width = self.canvas.getmaxyx()
        self._setup_game_window()

        self.position = 5
        self.coords = (1, 1)

        self.moves = []
        self.user_moves = []
        self.computer_moves = []

        self.game_status = 3

    def _init_colors(self):
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    def _setup_game_window(self):
        self.window = curses.newwin(self.height - 2, self.width - 2, 1, 1)
        self.window.nodelay(True)
        self.window.keypad(True)
        self.window.border()

    def _draw_game_field(self):
        self.fields = {}

        lines, cols = 5, 10
        begin_ys = (2, 6, 10)
        begin_xs = (2, 11, 20)
        curr_box_num = 1

        for begin_y in begin_ys:
            for begin_x in begin_xs:
                box = self.window.subwin(lines, cols, begin_y, begin_x)
                box.border()
                self.fields[curr_box_num] = box

                curr_box_num += 1

    def start_new_game(self):
        curses.curs_set(0)

        self._draw_game_field()

        curr_field = self.fields[self.position]
        curr_field.bkgd(' ', curses.color_pair(2))

        while True:
            key = self.window.getch()

            if key in DIRECTIONS:
                self._slide_field(*DIRECTIONS[key])
            elif key == 10:
                is_move_taken = self._user_move()
                if is_move_taken:
                    time.sleep(1)
                    self._computer_move()
            elif key == 27:
                time.sleep(1)
                curses.endwin()
                sys.exit(0)

    def _user_move(self):
        if self.position not in self.moves:
            self.moves.append(self.position)
            self.user_moves.append(self.position)
            field = self.fields[self.position]
            field.addstr(2, 3, 'user', curses.color_pair(1))
            field.refresh()

            self._check_game_status()
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

        field = self.fields[chosen_field]
        field.addstr(2, 3, 'comp', curses.color_pair(1))
        field.refresh()

        self._check_game_status()

    def _get_best_move(self, curr_move):
        for x, y, z in WINNING_COMBINATIONS:
            if x in self.computer_moves and y in self.computer_moves and z not in self.moves:
                return z
            if x in self.computer_moves and z in self.computer_moves and y not in self.moves:
                return y
            if y in self.computer_moves and z in self.computer_moves and x not in self.moves:
                return x

            if x in self.user_moves and y in self.user_moves and z not in self.moves:
                return z
            if x in self.user_moves and z in self.user_moves and y not in self.moves:
                return y
            if y in self.user_moves and z in self.user_moves and x not in self.moves:
                return x

        return curr_move

    def _check_game_status(self):
        self._set_game_status()

        if self.game_status == 3:
            return

        text = GAME_STATUSES[self.game_status]

        curses.flash()
        self.window.addstr(self.height // 2, self.width // 2, text, curses.color_pair(3))
        self.window.refresh()

        time.sleep(2)
        sys.exit(0)

    def _check_to_win(self, player):
        player_moves = self.user_moves if player == 'user' else self.computer_moves
        for winning_moves in WINNING_COMBINATIONS:
            is_win = all(map(lambda move: move in player_moves, winning_moves))
            if is_win:
                return True
        return False

    def _set_game_status(self):
        """
        Game statuses:
            0 - user win,
            1 - computer win,
            2 - tie,
            3 - game is not over
        """

        if self._check_to_win('user'):
            self.game_status = 0
        elif self._check_to_win('comp'):
            self.game_status = 1
        elif len(self.moves) == 9:
            self.game_status = 2
        else:
            self.game_status = 3

    def _slide_field(self, r, c):
        cols, rows = 3, 3
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
