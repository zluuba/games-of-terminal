from games_of_terminal.database.database import create_and_fill_db_tables
from games_of_terminal.interface_manager import InterfaceManager
from games_of_terminal.constants import KEYS, BASE_OFFSET, DEFAULT_COLOR
from games_of_terminal.log import log
from games_of_terminal.menu.constants import (
    TOP_SWORD_LEN, LOGO_MENU, LOGO_MENU_LEN,
    BOTTOM_SWORD_LEN, MENU_MAX_LEN, ANIMATION_SPEED,
    TOP_SWORD, BOTTOM_SWORD, SWORD_COLORS,
    CREATOR_NAME, GOODBYE_MESSAGES,
    FIRE_CHARS, FIRE_COLORS, FIRE_ELEMENTS_COUNT,
    MENU_ITEMS, MENU_ITEMS_COUNT, FIRE_CHARS_LEN,
)
from games_of_terminal.utils import (
    get_color_by_name, draw_message, hide_cursor,
)

from curses import endwin, flushinp, A_STANDOUT as REVERSE

from random import choice, random
from time import sleep
from sys import exit


class Menu(InterfaceManager):
    @log
    def __init__(self, canvas):
        super().__init__(canvas, only_main_win=True)

        create_and_fill_db_tables()
        self.current_row = 0

        self.setup_vars()

    def __repr__(self):
        return f'<Menu>'

    def setup_vars(self):
        self.height, self.width = self.canvas.getmaxyx()

        self.logo_start_y = (self.height // 2) - ((LOGO_MENU_LEN + MENU_ITEMS_COUNT) // 2) - 3
        self.menu_start_y = self.logo_start_y + LOGO_MENU_LEN + 3

        self.top_sword_y = self.logo_start_y - 1
        self.top_sword_x = (self.width // 2) - (TOP_SWORD_LEN // 2)

        self.bottom_sword_y = self.logo_start_y + LOGO_MENU_LEN
        self.bottom_sword_x = (self.width // 2) - (BOTTOM_SWORD_LEN // 2)

        self.fire_area_size = self.width * self.height
        self.fire_items = [0] * (self.fire_area_size + self.width + 1)

        end_offset = (BASE_OFFSET * 2) if (MENU_MAX_LEN % 2) else (BASE_OFFSET * 2 - 1)
        self.fire_free_area_begin_x = (self.width // 2) - (MENU_MAX_LEN // 2) - BASE_OFFSET
        self.fire_free_area_end_x = self.fire_free_area_begin_x + MENU_MAX_LEN + end_offset

        self.fire_animation_speed = ANIMATION_SPEED['medium']

        # self.logo_fill = choice(list(LOGO_FILL.values()))
        # self.default_logo_fill = LOGO_FILL['default']
        # self.logo_fill = LOGO_FILL['default']

    @log
    def run_menu_loop(self):
        self.initialize_menu()

        while True:
            key = self.window.getch()

            if key == KEYS['escape']:
                self.exit()
            elif key == KEYS['resize']:
                self.resize_menu_win_handler(key)
            elif key in (KEYS['up_arrow'], KEYS['w']):
                self.move_menu_selection(-1)
            elif key in (KEYS['down_arrow'], KEYS['s']):
                self.move_menu_selection(1)
            elif key in KEYS['enter']:
                self.run_selected_menu_item()

            self.update_menu_display()
            self.window.refresh()

    def redraw_window(self):
        self.setup_vars()
        self.initialize_menu()

    def initialize_menu(self):
        self.window.clear()
        hide_cursor()
        self.set_window_redrawing_speed()
        self.draw_menu()

    def move_menu_selection(self, direction):
        self.current_row = max(
            0, min(self.current_row + direction, MENU_ITEMS_COUNT - 1)
        )

    def update_menu_display(self):
        # redraw dynamic parts
        self.draw_fire_animation()
        self.show_menu_items_list()

    def draw_menu(self):
        # draw static parts
        self.draw_logo_with_swords()
        self.show_menu_items_list()
        self.draw_creator_name()
        self.window.refresh()

    def show_menu_items_list(self):
        begin_y = self.menu_start_y

        for row, menu_item in enumerate(MENU_ITEMS.values()):
            menu_item_name = menu_item['name']

            begin_y += 1 if menu_item_name == 'Settings' else 0
            y = begin_y + row
            x = (self.width // 2) - (len(menu_item_name) // 2)

            color = DEFAULT_COLOR + REVERSE if row == self.current_row \
                else DEFAULT_COLOR

            draw_message(y, x, self.window, menu_item_name, color)

    @log
    def run_selected_menu_item(self):
        chosen_menu_item = MENU_ITEMS[self.current_row]
        menu_item_name = chosen_menu_item['name']
        menu_item_class = chosen_menu_item['class']

        menu_item = menu_item_class(self.canvas, menu_item_name)
        menu_item.run()

        self.handle_post_running_actions()

    def handle_post_running_actions(self):
        flushinp()
        self.redraw_window()

    def draw_logo_with_swords(self):
        for y, line in enumerate(LOGO_MENU, start=self.logo_start_y):
            x = (self.width // 2) - (len(line) // 2)
            draw_message(y, x, self.window, line, DEFAULT_COLOR)

        self.draw_sword(TOP_SWORD, self.top_sword_y, self.top_sword_x)
        self.draw_sword(BOTTOM_SWORD, self.bottom_sword_y, self.bottom_sword_x)

    def draw_sword(self, sword, y, x):
        for name, part in sword:
            color = get_color_by_name(SWORD_COLORS[name])
            draw_message(y, x, self.window, part, color)
            x += len(part)

    def draw_creator_name(self):
        color = get_color_by_name('light_grey_text_black_bg')
        begin_y = self.height - 2
        begin_x = (self.width // 2) - (len(CREATOR_NAME) // 2)

        draw_message(begin_y, begin_x, self.window,
                     CREATOR_NAME, color)

    def draw_goodbye_message(self):
        goodbye_message = choice(GOODBYE_MESSAGES)
        begin_y = self.height // 2
        begin_x = (self.width // 2) - (len(goodbye_message) // 2)

        draw_message(begin_y, begin_x, self.window,
                     goodbye_message, DEFAULT_COLOR)

    def set_window_redrawing_speed(self):
        self.window.timeout(self.fire_animation_speed)

    def draw_fire_animation(self, animation=True, empty_middle=True):
        """
        A board (integer array) is created to reflect the size (width * height) of the screen.
        Then, each frame the board is translated upward (top row removed) and decayed (each integer is decremented)
        before a new, randomly seeded row is inserted at the bottom.
        """
        if not animation:
            return

        for i in range(self.width // 7):
            # self.width // 7 - affects the amount of fire. should be dynamic
            # AMOUNT_OF_FIRE_DIV ?
            index = int((random() * self.width) + self.width * (self.height - 1))
            self.fire_items[index] = FIRE_ELEMENTS_COUNT

        for i in range(self.fire_area_size):
            self.fire_items[i] = int(
                (self.fire_items[i] + self.fire_items[i + 1] + self.fire_items[i + self.width] +
                 + self.fire_items[i + self.width + 1]) / 4
            )
            color_name = ('yellow' if self.fire_items[i] > 15 else ('red' if self.fire_items[i] > 9 else 'black'))
            color = get_color_by_name(FIRE_COLORS[color_name])

            fire_char_index = min(self.fire_items[i], FIRE_CHARS_LEN - 1)
            char = FIRE_CHARS[fire_char_index]

            y = int(i / self.width)
            x = int(i % self.width)

            if i >= self.fire_area_size - 1:
                continue

            if empty_middle and (self.fire_free_area_begin_x <= x <= self.fire_free_area_end_x):
                continue

            self.window.addstr(y, x, char, color)

    @log
    def exit(self):
        self.window.clear()
        self.draw_goodbye_message()
        sleep(1)
        endwin()
        exit(0)
