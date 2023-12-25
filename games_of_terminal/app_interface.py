from curses import newwin, curs_set
from time import sleep

from .colors import Colors
from .field import Field
from .constants import *


class InterfaceManager(Colors):
    def __init__(self, canvas):
        super().__init__()

        self.canvas = canvas
        self._setup()

    def _setup(self):
        self.height, self.width = self.canvas.getmaxyx()
        self.canvas.bkgd(' ', self.default_color)
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

    def draw_logo(self):
        for y, line in enumerate(LOGO, start=1):
            self.draw_message(y, 2, self.logo_area.box, line, self.default_color)

        y, x = 6, (self.logo_area.width - len(APP_NAME)) // 2
        self.draw_message(y, x, self.logo_area.box, APP_NAME, self.default_color)

    @staticmethod
    def draw_message(begin_y, begin_x, field, message, color):
        field.addstr(begin_y, begin_x, message, color)
        field.refresh()

    @staticmethod
    def hide_cursor():
        curs_set(0)

    def wait_for_keypress(self):
        self.window.timeout(-1)

    def redraw_window(self):
        self.win_too_small_handle()
        self.window.clear()
        self.__init__(self.canvas)

    def is_window_too_small(self):
        return (self.height < MIN_WIN_HEIGHT or
                self.width < MIN_WIN_WIDTH)

    def win_too_small_handle(self):
        while self.is_window_too_small():
            self.show_win_too_small_msg()
            sleep(0.3)

            key = self.canvas.getch()
            self.wait_for_keypress()

            if key == KEYS['resize']:
                self.height, self.width = self.canvas.getmaxyx()

    def show_win_too_small_msg(self):
        message = 'Window is too small.'
        message_length = len(message)

        if message_length < self.width:
            return

        y = self.height // 2
        x = (self.width // 2) - (message_length // 2)
        self.draw_message(y, x, self.canvas, message, self.default_color)
        self.canvas.refresh()

    def _set_window_sizes(self):
        begin_x = begin_y = 0
        side_menu_width = len(LOGO[0]) + (BASE_OFFSET * 2)

        self.window_box_sizes = {
            'lines': self.height,
            'cols': self.width,
            'begin_y': begin_y,
            'begin_x': begin_x,
        }
        self.game_box_sizes = {
            'lines': self.height - BASE_OFFSET,
            'cols': self.width - side_menu_width,
            'begin_y': begin_y + DEFAULT_YX_OFFSET,
            'begin_x': begin_x,
        }
        self.side_menu_box_sizes = {
            'lines': self.height - BASE_OFFSET,
            'cols': side_menu_width,
            'begin_y': begin_y + DEFAULT_YX_OFFSET,
            'begin_x': self.width - side_menu_width,
        }
        self.logo_box_sizes = {
            'lines': len(LOGO) + BASE_OFFSET,
            'cols': side_menu_width,
            'begin_y': begin_y + DEFAULT_YX_OFFSET,
            'begin_x': self.width - side_menu_width,
        }
        self.status_box_sizes = {
            'lines': STATUS_BOX_HEIGHT + BASE_OFFSET,
            'cols': side_menu_width,
            'begin_y': self.height - (STATUS_BOX_HEIGHT + BASE_OFFSET + DEFAULT_YX_OFFSET),
            'begin_x': self.width - side_menu_width,
        }
        self.tips_box_sizes = {
            'lines': self.height - self.logo_box_sizes['lines'] - self.status_box_sizes['lines'],
            'cols': side_menu_width,
            'begin_y': self.logo_box_sizes['begin_y'] + self.logo_box_sizes['lines'] - 1,
            'begin_x': self.width - side_menu_width,
        }
