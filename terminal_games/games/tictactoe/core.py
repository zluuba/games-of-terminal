import curses
import random
import sys
import time


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

        self.position = 1
        self.coords = (0, 0)

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
        self.window.keypad(1)
        self.window.border()

    def _draw_game_field(self):
        one = self.window.subwin(5, 10, 2, 2)
        one.border()

        two = self.window.subwin(5, 10, 2, 12)
        two.border()

        three = self.window.subwin(5, 10, 2, 22)
        three.border()

        four = self.window.subwin(5, 10, 7, 2)
        four.border()

        five = self.window.subwin(5, 10, 7, 12)
        five.border()

        six = self.window.subwin(5, 10, 7, 22)
        six.border()

        seven = self.window.subwin(5, 10, 12, 2)
        seven.border()

        eight = self.window.subwin(5, 10, 12, 12)
        eight.border()

        nine = self.window.subwin(5, 10, 12, 22)
        nine.border()

        self.fields = {
            1: one, 2: two, 3: three,
            4: four, 5: five, 6: six,
            7: seven, 8: eight, 9: nine
        }

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

            is_game = self._check_game_status()
            if is_game is True:
                self.start_new_game()
            elif is_game is False:
                self._end_the_game()
            return True
        return False

    def _computer_move(self):
        chosen_field = None

        while chosen_field is None:
            move = random.randint(1, 9)
            if move not in self.moves:
                self.moves.append(move)
                self.computer_moves.append(move)
                chosen_field = move

        field = self.fields[chosen_field]
        field.addstr(2, 3, 'comp', curses.color_pair(1))
        field.refresh()

        self._check_game_status()

    def _check_user_to_win(self):
        for comb in WINNING_COMBINATIONS:
            is_win = all(map(lambda num: num in self.user_moves, comb))
            if is_win:
                return True
        return False

    def _check_computer_to_win(self):
        for comb in WINNING_COMBINATIONS:
            is_win = all(map(lambda num: num in self.computer_moves, comb))
            if is_win:
                return True
        return False

    def _check_game_status(self):
        self._set_game_status()

        if self.game_status == 3:
            return

        text = GAME_STATUSES[self.game_status]

        curses.flash()
        self.window.addstr(self.height // 2, self.width // 2, text, curses.color_pair(3))
        self.window.refresh()

        time.sleep(2)

        self._end_the_game()

    def _end_the_game(self):
        # curses.endwin()
        sys.exit(0)

    def _set_game_status(self):
        """
        Game statuses:
            0 - user win,
            1 - computer win,
            2 - tie,
            3 - game is not over
        """

        if self._check_user_to_win():
            self.game_status = 0
        elif self._check_computer_to_win():
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
            self._reset_fields()
            self._update_field()

    def _reset_fields(self):
        for pos, field in self.fields.items():
            field.bkgd(' ', curses.color_pair(1))
            field.refresh()

    def _update_field(self):
        window = self.fields[self.position]
        window.bkgd(' ', curses.color_pair(2))
        window.refresh()
