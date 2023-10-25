from games_of_terminal.games.constants import (
    MESSAGES, KEYS, LOGO_GOT, APP_NAME
)
import curses


class GameEngine:
    def __init__(self, canvas):
        self.canvas = canvas
        self._setup()

        self.state = {
            'pause': False,
            'game_status': 'game_is_on',
        }

        self.statuses = {
            'user_win': {'message': 'You WIN!', 'color': curses.color_pair(2)},
            'user_lose': {'message': 'You LOSE', 'color': curses.color_pair(3)},
            'tie': {'message': 'TIE', 'color': curses.color_pair(6)},
        }

    @property
    def game_status(self):
        # TODO: rebuild props - create 'is_user_win' func ?
        return self.state['game_status']

    @game_status.setter
    def game_status(self, status):
        self.state['game_status'] = status

    @staticmethod
    def _init_colors():
        # TODO: create variables to change lines
        #  from 'curses.color_pair(1)' to the 'white_text_red_bg'

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)     # white text, black bg
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)     # white text, green bg
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)       # white text, red bg
        curses.init_pair(4, curses.COLOR_WHITE, 236)                    # white text, dark grey bg
        curses.init_pair(5, curses.COLOR_WHITE, 245)                    # white text, light grey bg
        curses.init_pair(6, curses.COLOR_WHITE, 132)                    # white text, pink bg
        curses.init_pair(7, curses.COLOR_WHITE, 134)                    # white text, light purple bg

        curses.init_pair(8, curses.COLOR_RED, curses.COLOR_BLACK)       # red text, black bg
        curses.init_pair(9, curses.COLOR_GREEN, curses.COLOR_BLACK)     # green text, black bg
        curses.init_pair(10, curses.COLOR_YELLOW, curses.COLOR_BLACK)   # yellow text, black bg

        curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_RED)      # black text, red bg
        curses.init_pair(12, curses.COLOR_BLACK, 168)                   # black text, deep pink bg
        curses.init_pair(13, curses.COLOR_BLACK, 153)                   # black text, pastel dirty blue bg

        # minesweeper cells colors
        curses.init_pair(14, curses.COLOR_WHITE, 111)                   # white text, pastel blue bg
        curses.init_pair(15, curses.COLOR_WHITE, 75)                    # white text, light blue bg
        curses.init_pair(16, curses.COLOR_WHITE, 68)                    # white text, medium blue bg
        curses.init_pair(17, curses.COLOR_WHITE, 26)                    # white text, dark-medium blue bg
        curses.init_pair(18, curses.COLOR_WHITE, 17)                    # white text, deep blue bg
        curses.init_pair(19, curses.COLOR_WHITE, 54)                    # white text, deep purple bg

    def _setup(self):
        self.height, self.width = self.canvas.getmaxyx()

        # set black background
        # TODO: add ability to change themes - black/white (?)
        self.canvas.bkgd(' ', curses.color_pair(1))

        self._init_colors()
        self._setup_sizes()

        self._draw_window()
        self._setup_boxes()
        self._setup_side_menu()

    def _setup_boxes(self):
        self.game_box = self._draw_box(self.game_box_sizes)
        self.game_box_height, self.game_box_width = self.game_box.getmaxyx()

        self.side_menu_box = self._draw_box(self.side_menu_box_sizes)
        self.side_menu_box_height, self.side_menu_box_width = self.side_menu_box.getmaxyx()

        self.logo_box = self._draw_box(self.logo_box_sizes)
        self.logo_box_height, self.logo_box_width = self.logo_box.getmaxyx()

    def _setup_side_menu(self):
        # TODO: add tips, rules, hotkeys
        self._draw_logo()

    def _draw_box(self, sizes):
        box = self.window.subwin(*sizes.values())
        box.border()
        return box

    def _draw_window(self):
        sizes = self.window_box_sizes.values()
        self.window = curses.newwin(*sizes)
        self.window.nodelay(True)
        self.window.keypad(True)

    def _draw_logo(self):
        for y, line in enumerate(LOGO_GOT, start=1):
            self._draw_message(y, 2, self.logo_box, line, curses.color_pair(1))

        y, x = 6, (self.logo_box_width - len(APP_NAME)) // 2
        self._draw_message(y, x, self.logo_box, APP_NAME, curses.color_pair(1))

    def _wait(self):
        self.window.timeout(-1)

    @staticmethod
    def _hide_cursor():
        curses.curs_set(0)

    def _pause(self):
        self.state['pause'] = not self.state['pause']
        self._wait()

        if self.state['pause']:
            self._show_pause_message()
            key = self.window.getch()

            while key != KEYS['pause']:
                self._wait()
                key = self.window.getch()

        self.window.timeout(150)
        return

    def _show_pause_message(self):
        message = ' PAUSE '

        x = (self.game_box_width // 2 + self.game_box_sizes['begin_x']) - (len(message) // 2)
        y = self.game_box_height // 2 + self.game_box_sizes['begin_y']

        self._draw_message(y, x, self.game_box, message, curses.color_pair(10))

    def _show_who_won(self):
        message = self.statuses[self.game_status]['message']
        color = self.statuses[self.game_status]['color']

        y, x = self.side_menu_box_height - 2, 1
        empty_line = ' ' * (self.side_menu_box_width - 2)

        for offset in range(0, -3, -1):
            new_y = y + offset
            self._draw_message(new_y, x, self.side_menu_box, empty_line, color)

        middle_x = (self.side_menu_box_width // 2) - len(message) // 2
        self._draw_message(y - 1, middle_x, self.side_menu_box, message, color)

    def _is_restart(self):
        # TODO: add transparent background color func
        """ Draws a message in the center of the playing field
        that the user can restart the game,
        waiting for a response (space bar pressing)
        """

        message = f" {MESSAGES['play_again']} "

        x = (self.game_box_width // 2) - (len(message) // 2)
        y = self.game_box_height // 2

        self._draw_message(y, x, self.game_box, message, curses.A_BLINK)

        self._wait()
        curses.flushinp()
        key = self.window.getch()

        if key == KEYS['space']:
            self.game_box.erase()
            return True
        return False

    @staticmethod
    def _draw_message(y, x, field, message, color):
        field.addstr(y, x, message, color)
        field.refresh()

    def _setup_sizes(self):
        self.game_box_sizes = {
            'lines': self.height - 2,
            'cols': self.width - 27,
            'begin_y': 1,
            'begin_x': 0,
        }

        self.side_menu_box_sizes = {
            'lines': self.height - 8,
            'cols': 27,
            'begin_y': 7,
            'begin_x': self.width - 27,
        }

        self.logo_box_sizes = {
            'lines': 7,
            'cols': 27,
            'begin_y': 1,
            'begin_x': self.width - 27,
        }

        self.window_box_sizes = {
            'lines': self.height,
            'cols': self.width,
            'begin_y': 0,
            'begin_x': 0,
        }
