from games_of_terminal.interface_manager import InterfaceManager
from games_of_terminal.sub_window import SubWindow

from games_of_terminal.constants import (
    ITEMS, KEYS, BASE_OFFSET, DEFAULT_COLOR,
)
from games_of_terminal.database.database import get_all_settings
from games_of_terminal.utils import (
    draw_message, hide_cursor,
)
from games_of_terminal.settings.all_settings.constants import (
    TITLE, TOP_OFFSET,
)

from curses import A_STANDOUT as REVERSE


class GamesSettings(InterfaceManager):
    def __init__(self, canvas, name):
        super().__init__(canvas, only_main_win=True)

        self.name = name
        self.current_row = 0

        self.all_settings = get_all_settings()
        self.setup_vars()

    def setup_vars(self):
        self.items_len = len(ITEMS)

        self.title_start_y = TOP_OFFSET
        self.settings_start_y = self.get_settings_start_y()

        self.sub_windows_height = self.height - self.settings_start_y - 1

        self.items_list_width = self.width // 4
        self.items_list_begin_y = self.settings_start_y
        self.items_list_begin_x = BASE_OFFSET // 2

        self.settings_area_width = self.width - self.items_list_width - BASE_OFFSET - 1
        self.settings_area_begin_y = self.settings_start_y
        self.settings_area_begin_x = self.items_list_begin_x + self.items_list_width + 1

    def get_settings_start_y(self):
        return self.title_start_y + len(TITLE) + 1

    def run(self):
        self.initialize_settings()

        while True:
            key = self.window.getch()
            self.wait_for_keypress()

            if key == KEYS['escape']:
                return
            # elif key == KEYS['resize']:
            #     self.window.timeout(0)
            #     self.resize_menu_win_handler(key)
            elif key in (KEYS['up_arrow'], KEYS['w']):
                self.move_menu_selection(-1)
            elif key in (KEYS['down_arrow'], KEYS['s']):
                self.move_menu_selection(1)
            elif key in KEYS['enter']:
                self.go_to_selected_settings()

            self.update_settings_display()
            self.window.refresh()

    def go_to_selected_settings(self):
        pass

    def update_settings_display(self):
        # draw dynamic parts
        self.show_settings_items_list()
        self.show_selected_settings()

    def show_settings_items_list(self):
        begin_y = 1

        for row, settings_item in enumerate(ITEMS):
            y = begin_y + row
            x = (self.items_list_width // 2) - (len(settings_item) // 2)
            color = DEFAULT_COLOR + REVERSE if row == self.current_row \
                else DEFAULT_COLOR

            draw_message(y, 1, self.items_list_area.box, ' ' * (self.items_list_width - 2), color)
            draw_message(y, x, self.items_list_area.box, settings_item, color)

    def show_selected_settings(self):
        self.settings_area.box.clear()
        self.settings_area.show_borders()

        curr_settings = self.all_settings[ITEMS[self.current_row]]
        draw_message(1, 1, self.settings_area.box, str(curr_settings))

    def initialize_settings(self):
        hide_cursor()
        self.window.clear()
        self.setup_sub_windows()
        self.show_settings_title()
        self.update_settings_display()
        self.window.refresh()

    def show_settings_title(self):
        for y, line in enumerate(TITLE, start=self.title_start_y):
            x = (self.width // 2) - (len(line) // 2)
            draw_message(y, x, self.window, line)

    def setup_sub_windows(self):
        self.items_list_area = SubWindow(
            self.window, self.sub_windows_height, self.items_list_width,
            self.items_list_begin_y, self.items_list_begin_x,
        )

        self.settings_area = SubWindow(
            self.window, self.sub_windows_height, self.settings_area_width,
            self.settings_area_begin_y, self.settings_area_begin_x,
        )

    def move_menu_selection(self, direction):
        new_current_row = self.current_row + direction

        if new_current_row < 0:
            self.current_row = len(ITEMS) - 1
        elif new_current_row >= len(ITEMS):
            self.current_row = 0
        else:
            self.current_row = new_current_row
