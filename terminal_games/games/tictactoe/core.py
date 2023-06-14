from curses import textpad
import curses

import sys


class TicTacToeGame:
    def __init__(self, canvas):
        self.screen_height, self.screen_width = canvas.getmaxyx()
        self.canvas = canvas
        self.box = []

    def set_game_area(self, top, bottom, left, right):
        self.box = [[top, bottom],
                    [self.screen_height - left, self.screen_width - right]]
        textpad.rectangle(self.canvas, *self.box[0], *self.box[1])

    def start_new_game(self):
        curses.curs_set(0)
        self.set_game_area(3, 3, 3, 4)

        elem_skin_x = '-'
        elem_skin_y = '|'
        elem_size = 6
        border_size = 3

        # border = []

        # show game desk - x
        self.canvas.addstr(
            (self.screen_height // 2) - border_size // 2,
            self.screen_width // 2 - elem_size * 3 // 2,
            elem_skin_x * (elem_size * 3 + 1),
        )
        self.canvas.addstr(
            (self.screen_height // 2) + border_size // 2 + 1,
            self.screen_width // 2 - elem_size * 3 // 2,
            elem_skin_x * (elem_size * 3 + 1),
        )

        # show game desk - y
        y = self.screen_height // 2 + 4
        for _ in range(8):
            self.canvas.addstr(
                y,
                self.screen_width // 2 - 3,
                elem_skin_y,
            )
            y -= 1
            self.canvas.refresh()

        y = self.screen_height // 2 + 4
        for _ in range(8):
            self.canvas.addstr(
                y,
                self.screen_width // 2 + 3,
                elem_skin_y,
            )
            y -= 1
            self.canvas.refresh()

        while True:
            key = self.canvas.getch()
            if key == curses.KEY_RIGHT:
                sys.exit(0)
