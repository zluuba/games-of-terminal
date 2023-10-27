from games_of_terminal.colors import Colors
from games_of_terminal.constants import (
    LOGO, APP_NAME,
)
import curses


class InterfaceManager(Colors):
    def __init__(self, canvas):
        super().__init__()

        self.canvas = canvas
        self._setup()

    def _setup(self):
        self.height, self.width = self.canvas.getmaxyx()

        canvas_bg_color = self.get_color_by_name('white_text_black_bg')
        self.canvas.bkgd(' ', canvas_bg_color)

        self._set_window_sizes()
        self._draw_main_window()
        self._setup_subwindows()
        self.hide_cursor()

    def _draw_main_window(self):
        sizes = self.window_box_sizes.values()
        self.window = curses.newwin(*sizes)
        self.window.nodelay(True)
        self.window.keypad(True)

    def _get_subwindow_with_borders(self, sizes_dict):
        sizes = sizes_dict.values()
        subwindow = self.window.subwin(*sizes)
        subwindow.border()
        return subwindow

    def _setup_subwindows(self):
        self.game_box = self._get_subwindow_with_borders(self.game_box_sizes)
        self.game_box_height, self.game_box_width = self.game_box.getmaxyx()

        self.side_menu_box = self._get_subwindow_with_borders(self.side_menu_box_sizes)
        self.side_menu_box_height, self.side_menu_box_width = self.side_menu_box.getmaxyx()

        self.logo_box = self._get_subwindow_with_borders(self.logo_box_sizes)
        self.logo_box_height, self.logo_box_width = self.logo_box.getmaxyx()

    def _setup_side_menu(self):
        self._draw_logo()
        # self._draw_tips

    def _draw_logo(self):
        color = self.get_color_by_name('white_text_black_bg')

        for y, line in enumerate(LOGO, start=1):
            self.draw_message(y, 2, self.logo_box, line, color)

        y, x = 6, (self.logo_box_width - len(APP_NAME)) // 2
        self.draw_message(y, x, self.logo_box, APP_NAME, color)

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
