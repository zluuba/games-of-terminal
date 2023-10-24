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

    @property
    def game_status(self):
        return self.state['game_status']

    @game_status.setter
    def game_status(self, status):
        self.state['game_status'] = status

    @staticmethod
    def _init_colors():
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)     # white text, black bg
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)     # white text, green bg
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)       # white text, red bg
        curses.init_pair(4, 1, 236)                                     # dark grey
        curses.init_pair(5, 1, 245)                                     # light grey
        curses.init_pair(6, 1, 132)                                     # pink
        curses.init_pair(7, 1, 134)                                     # light purple

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
        self.canvas.bkgd(' ', curses.color_pair(1))

        self._init_colors()
        self._setup_sizes()

        self._draw_window()
        self._setup_boxes()
        self._draw_logo()

    def _setup_boxes(self):
        self.game_box = self._draw_box(self.sizes['game_box'])
        self.game_box_height, self.game_box_width = self.game_box.getmaxyx()

        self.side_menu_box = self._draw_box(self.sizes['side_menu_box'])
        self.side_menu_box_height, self.side_menu_box_width = self.side_menu_box.getmaxyx()

        self.logo_box = self._draw_box(self.sizes['logo_box'])
        self.logo_box_height, self.logo_box_width = self.logo_box.getmaxyx()

    def _draw_box(self, sizes):
        box = self.window.subwin(*sizes.values())
        box.border()
        return box

    def _draw_window(self):
        sizes = self.sizes['window_box'].values()
        self.window = curses.newwin(*sizes)
        self.window.nodelay(True)
        self.window.keypad(True)

    def _draw_logo(self):
        y, x = 1, 2

        for line in LOGO_GOT:
            self.logo_box.addstr(y, x, line)
            y += 1

        begin_x = (self.logo_box_width - len(APP_NAME)) // 2
        self.logo_box.addstr(6, begin_x, APP_NAME)

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

        middle_x = self.game_box_width // 2 + self.sizes['game_box']['begin_x']
        middle_y = self.game_box_height // 2 + self.sizes['game_box']['begin_y']

        self.game_box.addstr(middle_y, middle_x - (len(message) // 2), message, curses.color_pair(10))
        self.game_box.refresh()

    def _draw_game_over_message(self, y=1, x=1):
        message = MESSAGES['game_over']

        for offset in range(3):
            self.game_box.addstr(
                y + offset,
                x,
                ' ' * (self.game_box_width - 2),
                curses.color_pair(11),
            )

        self.game_box.addstr(
            y + 1,
            (self.game_box_width // 2) - len(message) // 2,
            message,
            curses.color_pair(11),
        )

        self.game_box.nodelay(True)
        self.game_box.refresh()

    def _is_restart(self):
        message = MESSAGES['play_again']
        self.side_menu_box.addstr(
            self.side_menu_box_height // 2 + 2,
            self.side_menu_box_width // 2 - len(message) // 2,
            message, curses.A_BLINK + curses.color_pair(1),
        )

        self.side_menu_box.refresh()

        curses.flushinp()
        self._wait()
        key = self.window.getch()

        if key == KEYS['space']:
            self.game_box.erase()
            return True
        return False

    def _setup_sizes(self):
        self.sizes = {
            'game_box': {
                'lines': self.height - 2,
                'cols': self.width - 27,
                'begin_y': 1,
                'begin_x': 0,
            },
            'side_menu_box': {
                'lines': self.height - 8,
                'cols': 27,
                'begin_y': 7,
                'begin_x': self.width - 27,
            },
            'logo_box': {
                'lines': 7,
                'cols': 27,
                'begin_y': 1,
                'begin_x': self.width - 27,
            },
            'window_box': {
                'lines': self.height,
                'cols': self.width,
                'begin_y': 0,
                'begin_x': 0,
            },
        }
