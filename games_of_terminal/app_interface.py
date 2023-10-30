from games_of_terminal.colors import Colors
from games_of_terminal.constants import (
    LOGO, APP_NAME, SIDE_MENU_TIPS,
)
from games_of_terminal.field import Field
import curses


class InterfaceManager(Colors):
    def __init__(self, canvas):
        super().__init__()

        self.canvas = canvas
        self._setup()

    def _setup(self):
        self.hide_cursor()
        self.canvas.bkgd(' ', self.default_color)

        self.height, self.width = self.canvas.getmaxyx()

        self._set_window_sizes()
        self._init_main_window()
        self._init_subwindows()

    def _init_main_window(self):
        window_sizes = self.window_box_sizes.values()

        self.window = curses.newwin(*window_sizes)
        self.window.nodelay(True)
        self.window.keypad(True)

    def _init_subwindows(self):
        self.game_area = Field(self.window, *self.game_box_sizes.values())
        self.side_menu = Field(self.window, *self.side_menu_box_sizes.values())
        self.tips = Field(self.side_menu.box, *self.tips_box_sizes.values())
        self.logo = Field(self.side_menu.box, *self.logo_box_sizes.values())
        self.game_status_area = Field(self.side_menu.box, *self.status_box_sizes.values())

    def _setup_side_menu(self):
        self._draw_logo()
        self.draw_side_menu_tips()

    def _draw_logo(self):
        for y, line in enumerate(LOGO, start=1):
            self.draw_message(y, 2, self.logo.box, line, self.default_color)

        y, x = 6, (self.logo.width - len(APP_NAME)) // 2
        self.draw_message(y, x, self.logo.box, APP_NAME, self.default_color)

    def draw_side_menu_tips(self, y=2, x=2, tips=None):
        if tips is None:
            tips = SIDE_MENU_TIPS

        for key, description in tips.items():
            self._clear_line(y, x, self.tips.box, (self.tips.width - (x * 2)))

            message = f'{key} - {description}'
            self.draw_message(y, x, self.tips.box, message, self.default_color)
            y += 1

    def _clear_line(self, y, x, field, width):
        empty_line = ' ' * width
        self.draw_message(y, x, field, empty_line, self.default_color)
        field.refresh()

    @staticmethod
    def draw_message(y, x, field, message, color):
        field.addstr(y, x, message, color)
        field.refresh()

    @staticmethod
    def hide_cursor():
        curses.curs_set(0)

    def wait_for_keypress(self):
        self.window.timeout(-1)

    def _set_window_sizes(self):
        self.window_box_sizes = {
            'lines': self.height,
            'cols': self.width,
            'begin_y': 0,
            'begin_x': 0,
        }

        self.game_box_sizes = {
            'lines': self.height - 2,
            'cols': self.width - 27,
            'begin_y': 1,
            'begin_x': 0,
        }

        self.side_menu_box_sizes = {
            'lines': self.height - 2,
            'cols': 27,
            'begin_y': 1,
            'begin_x': self.width - 27,
        }

        self.logo_box_sizes = {
            'lines': 7,
            'cols': 27,
            'begin_y': 1,
            'begin_x': self.width - 27,
        }

        self.status_box_sizes = {
            'lines': 5,
            'cols': 27,
            'begin_y': self.height - 6,
            'begin_x': self.width - 27,
        }

        self.tips_box_sizes = {
            'lines': self.height - self.logo_box_sizes['lines'] - self.status_box_sizes['lines'],
            'cols': 27,
            'begin_y': self.logo_box_sizes['begin_y'] + self.logo_box_sizes['lines'] - 1,
            'begin_x': self.width - 27,
        }
