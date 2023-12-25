from games_of_terminal.app_interface import InterfaceManager
from games_of_terminal.constants import KEYS, BASE_OFFSET
from games_of_terminal.database.database import create_db_tables
from games_of_terminal.menu.constants import *

from curses import flushinp, A_STANDOUT as REVERSE

from random import choice, random
from time import sleep
from sys import exit


class Menu(InterfaceManager):
    def _setup(self):
        super()._setup()
        create_db_tables()

        self.current_row = 0

        self.logo_start_y = (self.height // 2) - ((len(LOGO_MENU) + len(GAMES)) // 2) - 3
        self.menu_start_y = self.logo_start_y + len(LOGO_MENU) + 3

        self.top_sword_y = self.logo_start_y - 1
        self.top_sword_x = (self.width // 2) - (TOP_SWORD_LEN // 2)

        self.bottom_sword_y = self.logo_start_y + len(LOGO_MENU)
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

    def run_menu_loop(self):
        self.initialize_menu()

        while True:
            key = self.window.getch()

            if key == KEYS['escape']:
                self.exit()
            elif key == KEYS['resize']:
                self.redraw_window()
            elif key in (KEYS['up_arrow'], KEYS['w']):
                self.move_menu_selection(-1)
            elif key in (KEYS['down_arrow'], KEYS['s']):
                self.move_menu_selection(1)
            elif key in KEYS['enter']:
                self.start_selected_game()

            self.update_menu_display()
            self.window.refresh()

    def initialize_menu(self):
        self.window.clear()
        self.hide_cursor()
        self.set_window_redrawing_speed()
        self.draw_menu()

    def move_menu_selection(self, direction):
        self.current_row = max(
            0, min(self.current_row + direction, MENU_LENGTH - 1)
        )

    def update_menu_display(self):
        # redraw dynamic parts
        self.draw_fire_animation()
        self.show_games_list()

    def draw_menu(self):
        # draw static parts
        self.draw_logo_with_swords()
        self.show_games_list()
        self.draw_creator_name()
        self.window.refresh()

    def show_games_list(self):
        begin_y = self.menu_start_y

        for row, game in enumerate(GAMES.values()):
            game_name = game['name']

            begin_y += 1 if game_name == 'Settings' else 0
            y = begin_y + row
            x = (self.width // 2) - (len(game_name) // 2)

            color = self.default_color + REVERSE if row == self.current_row \
                else self.default_color

            self.draw_message(y, x, self.window, game_name, color)

    def start_selected_game(self):
        chosen_game = GAMES[self.current_row]
        game_name = chosen_game['name']
        game_class = chosen_game['game']

        game = game_class(self.canvas, game_name)
        game.run()

        self.handle_post_game()

    def handle_post_game(self):
        flushinp()
        self.initialize_menu()

    def draw_logo_with_swords(self):
        for y, line in enumerate(LOGO_MENU, start=self.logo_start_y):
            x = (self.width // 2) - (len(line) // 2)
            self.draw_message(y, x, self.window, line, self.default_color)

        self.draw_sword(TOP_SWORD, self.top_sword_y, self.top_sword_x)
        self.draw_sword(BOTTOM_SWORD, self.bottom_sword_y, self.bottom_sword_x)

    def draw_sword(self, sword, y, x):
        for name, part in sword:
            color = self.get_color_by_name(SWORD_COLORS[name])
            self.draw_message(y, x, self.window, part, color)
            x += len(part)

    def draw_creator_name(self):
        color = self.get_color_by_name('light_grey_text_black_bg')
        begin_y = self.height - 2
        begin_x = (self.width // 2) - (len(CREATOR_NAME) // 2)

        self.draw_message(begin_y, begin_x, self.window,
                          CREATOR_NAME, color)

    def draw_goodbye_message(self):
        goodbye_message = choice(GOODBYE_MESSAGES)
        begin_y = self.height // 2
        begin_x = (self.width // 2) - (len(goodbye_message) // 2)

        self.draw_message(begin_y, begin_x, self.window,
                          goodbye_message, self.default_color)

    def set_window_redrawing_speed(self):
        self.window.timeout(self.fire_animation_speed)

    def draw_fire_animation(self, animation=True, empty_middle=True):
        if not animation:
            return

        for i in range(int(self.width / 9)):
            index = int((random() * self.width) + self.width * (self.height - 1))
            self.fire_items[index] = FIRE_ELEMENTS_COUNT

        for i in range(self.fire_area_size):
            self.fire_items[i] = int(
                (self.fire_items[i] + self.fire_items[i + 1] + self.fire_items[i + self.width] +
                 + self.fire_items[i + self.width + 1]) / 4
            )
            color_name = ('yellow' if self.fire_items[i] > 15 else ('red' if self.fire_items[i] > 9 else 'black'))
            color = self.get_color_by_name(FIRE_COLORS[color_name])

            fire_char_index = LAST_FIRE_CHAR_IND if self.fire_items[i] > LAST_FIRE_CHAR_IND else self.fire_items[i]
            char = FIRE_CHARS[fire_char_index]

            y = int(i / self.width)
            x = int(i % self.width)

            if i >= self.fire_area_size - 1:
                continue

            if empty_middle and (self.fire_free_area_begin_x <= x <= self.fire_free_area_end_x):
                continue

            self.window.addstr(y, x, char, color)

    def exit(self):
        self.window.clear()
        self.draw_goodbye_message()
        sleep(1)
        exit(0)
