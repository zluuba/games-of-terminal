from games_of_terminal.colors import Colors
from games_of_terminal.constants import (
    LOGO, APP_NAME, SIDE_MENU_TIPS, STATUS_BOX_SIZE,
    DEFAULT_OFFSET, DEFAULT_Y_OFFSET,
)
from games_of_terminal.field import Field

from curses import newwin, curs_set


class InterfaceManager(Colors):
    def __init__(self, canvas):
        super().__init__()

        self.canvas = canvas
        self._setup()

    def _setup(self):
        self.canvas.bkgd(' ', self.default_color)
        self.height, self.width = self.canvas.getmaxyx()

        self._set_window_sizes()
        self._init_main_window()
        self._init_subwindows()

    def _init_main_window(self):
        window_sizes = self.window_box_sizes.values()

        self.window = newwin(*window_sizes)
        self.window.nodelay(True)
        self.window.keypad(True)

    def _init_subwindows(self):
        self.game_area = Field(self.window, *self.game_box_sizes.values())
        self.side_menu = Field(self.window, *self.side_menu_box_sizes.values())

        self.tips_area = Field(self.side_menu.box, *self.tips_box_sizes.values())
        self.logo_area = Field(self.side_menu.box, *self.logo_box_sizes.values())
        self.game_status_area = Field(self.side_menu.box, *self.status_box_sizes.values())

    def setup_side_menu(self):
        self._draw_logo()
        self.draw_side_menu_tips()

    def _draw_logo(self):
        for y, line in enumerate(LOGO, start=1):
            self.draw_message(y, 2, self.logo_area.box, line, self.default_color)

        y, x = 6, (self.logo_area.width - len(APP_NAME)) // 2
        self.draw_message(y, x, self.logo_area.box, APP_NAME, self.default_color)

    def draw_side_menu_tips(self, y=2, x=2, tips=None, color=None):
        if tips is None:
            tips = SIDE_MENU_TIPS

        if color is None:
            color = self.default_color

        for key, description in tips.items():
            self._clear_line(y, x, self.tips_area.box, (self.tips_area.width - (x * 2)))

            message = f'{key} - {description}'
            self.draw_message(y, x, self.tips_area.box, message, color)
            y += 1

    def _clear_line(self, y, x, field, width):
        empty_line = ' ' * width
        self.draw_message(y, x, field, empty_line, self.default_color)

    @staticmethod
    def draw_message(y, x, field, message, color):
        field.addstr(y, x, message, color)
        field.refresh()

    @staticmethod
    def hide_cursor():
        curs_set(0)

    def wait_for_keypress(self):
        self.window.timeout(-1)

    def resize_window(self):
        self.window.clear()
        self._setup()

    def _set_window_sizes(self):
        begin_x = begin_y = 0
        side_menu_width = len(LOGO[0]) + (DEFAULT_OFFSET * 2)

        self.window_box_sizes = {
            'lines': self.height,
            'cols': self.width,
            'begin_y': begin_y,
            'begin_x': begin_x,
        }
        self.game_box_sizes = {
            'lines': self.height - DEFAULT_OFFSET,
            'cols': self.width - side_menu_width,
            'begin_y': begin_y + DEFAULT_Y_OFFSET,
            'begin_x': begin_x,
        }
        self.side_menu_box_sizes = {
            'lines': self.height - DEFAULT_OFFSET,
            'cols': side_menu_width,
            'begin_y': begin_y + DEFAULT_Y_OFFSET,
            'begin_x': self.width - side_menu_width,
        }
        self.logo_box_sizes = {
            'lines': len(LOGO) + DEFAULT_OFFSET,
            'cols': side_menu_width,
            'begin_y': begin_y + DEFAULT_Y_OFFSET,
            'begin_x': self.width - side_menu_width,
        }
        self.status_box_sizes = {
            'lines': STATUS_BOX_SIZE + DEFAULT_OFFSET,
            'cols': side_menu_width,
            'begin_y': self.height - (STATUS_BOX_SIZE + DEFAULT_OFFSET + DEFAULT_Y_OFFSET),
            'begin_x': self.width - side_menu_width,
        }
        self.tips_box_sizes = {
            'lines': self.height - self.logo_box_sizes['lines'] - self.status_box_sizes['lines'],
            'cols': side_menu_width,
            'begin_y': self.logo_box_sizes['begin_y'] + self.logo_box_sizes['lines'] - 1,
            'begin_x': self.width - side_menu_width,
        }
