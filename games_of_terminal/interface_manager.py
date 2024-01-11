from games_of_terminal.constants import (
    LOGO, APP_NAME, KEYS,
    BASE_OFFSET, DEFAULT_YX_OFFSET, STATUS_BOX_HEIGHT,
    DEFAULT_COLOR, MESSAGES,
)
from games_of_terminal.sub_window import SubWindow
from games_of_terminal.utils import (
    draw_message, init_curses_colors,
    too_small_window_handler,
)

from curses import newwin
from time import sleep


class InterfaceManager:
    def __init__(self, canvas, only_main_win=False):
        init_curses_colors()

        self.canvas = canvas
        self._setup(only_main_win=only_main_win)

    def _setup(self, only_main_win=False):
        self.height, self.width = self.canvas.getmaxyx()
        too_small_window_handler(self.height, self.width)
        self.canvas.bkgd(' ', DEFAULT_COLOR)

        self._set_window_sizes()
        self._init_main_window()

        if not only_main_win:
            self._init_subwindows()

    def _init_main_window(self):
        window_sizes = self.window_box_sizes.values()
        self.window = newwin(*window_sizes)
        self.window.nodelay(True)
        self.window.keypad(True)

    def _init_subwindows(self):
        self.game_area = SubWindow(self.window, *self.game_box_sizes.values())
        self.side_menu = SubWindow(self.window, *self.side_menu_box_sizes.values())
        self.tips_area = SubWindow(self.side_menu.box, *self.tips_box_sizes.values())
        self.logo_area = SubWindow(self.side_menu.box, *self.logo_box_sizes.values())
        self.game_status_area = SubWindow(self.side_menu.box, *self.status_box_sizes.values())

    def draw_logo(self):
        for y, line in enumerate(LOGO, start=1):
            draw_message(y, 2, self.logo_area.box, line, DEFAULT_COLOR)

        y, x = 6, (self.logo_area.width - len(APP_NAME)) // 2
        draw_message(y, x, self.logo_area.box, APP_NAME, DEFAULT_COLOR)

    def wait_for_keypress(self):
        self.window.timeout(-1)

    def resize_menu_win_handler(self, key):
        message = MESSAGES['win_resize_menu']

        while key == KEYS['resize']:
            self.window.clear()
            new_height, new_width = self.canvas.getmaxyx()
            too_small_window_handler(new_height, new_width)

            y = self.height // 2
            x = (self.width // 2) - (len(message) // 2)

            draw_message(y, x, self.window, message, DEFAULT_COLOR)
            self.height, self.width = new_height, new_width
            sleep(0.1)

            key = self.window.getch()

        self.redraw_window()

    def resize_game_win_handler(self, key):
        messages = MESSAGES['win_resize_game']

        while key == KEYS['resize']:
            self.window.clear()
            new_height, new_width = self.canvas.getmaxyx()
            too_small_window_handler(new_height, new_width)
            start_y = new_height // 2

            for y_offset, message in enumerate(messages):
                y = start_y + y_offset
                x = (new_width // 2) - (len(message) // 2)
                draw_message(y, x, self.window, message, DEFAULT_COLOR)

            self.height, self.width = new_height, new_width
            sleep(0.3)

            key = self.window.getch()

        sleep(0.5)
        self._set_window_sizes()
        self._setup()

    def redraw_window(self):
        pass

    def _set_window_sizes(self, height=None, width=None):
        if not height:
            height = self.height
        if not width:
            width = self.width

        begin_x = begin_y = 0
        side_menu_width = len(LOGO[0]) + (BASE_OFFSET * 2)

        self.window_box_sizes = {
            'lines': height,
            'cols': width,
            'begin_y': begin_y,
            'begin_x': begin_x,
        }
        self.game_box_sizes = {
            'lines': height - BASE_OFFSET,
            'cols': width - side_menu_width,
            'begin_y': begin_y + DEFAULT_YX_OFFSET,
            'begin_x': begin_x,
        }
        self.side_menu_box_sizes = {
            'lines': height - BASE_OFFSET,
            'cols': side_menu_width,
            'begin_y': begin_y + DEFAULT_YX_OFFSET,
            'begin_x': width - side_menu_width,
        }
        self.logo_box_sizes = {
            'lines': len(LOGO) + BASE_OFFSET,
            'cols': side_menu_width,
            'begin_y': begin_y + DEFAULT_YX_OFFSET,
            'begin_x': width - side_menu_width,
        }
        self.status_box_sizes = {
            'lines': STATUS_BOX_HEIGHT + BASE_OFFSET,
            'cols': side_menu_width,
            'begin_y': height - (STATUS_BOX_HEIGHT + BASE_OFFSET + DEFAULT_YX_OFFSET),
            'begin_x': width - side_menu_width,
        }
        self.tips_box_sizes = {
            'lines': height - self.logo_box_sizes['lines'] - self.status_box_sizes['lines'],
            'cols': side_menu_width,
            'begin_y': self.logo_box_sizes['begin_y'] + self.logo_box_sizes['lines'] - 1,
            'begin_x': width - side_menu_width,
        }
