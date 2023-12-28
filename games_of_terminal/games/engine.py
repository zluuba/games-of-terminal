from games_of_terminal.database.database import update_game_state
from games_of_terminal.app_interface import InterfaceManager
from games_of_terminal.field import Field
from games_of_terminal.utils import (
    get_game_tips, draw_message,
    clear_field_line, get_color_by_name,
)
from games_of_terminal.constants import (
    MESSAGES, KEYS, GAME_STATUSES, BASE_OFFSET,
)
from games_of_terminal.games.game_stats import GameStats

from curses import flash, flushinp, endwin, A_BLINK as BLINK
from time import sleep


class GameEngine(InterfaceManager):
    def __init__(self, canvas, game_name):
        super().__init__(canvas)
        self.game_name = game_name
        self.stats = GameStats()

    def run(self):
        while True:
            self.setup_game_stats()
            self.setup_game_field()
            self.start_new_game()

            if self.stats.is_exit or not self.stats.is_restart:
                break

            self.reset_game_area()
            self.reset_game_stats()

    def reset_game_area(self):
        self.game_area.box.erase()
        self.game_area = Field(self.window, *self.game_box_sizes.values())
        self.game_area.box.refresh()

    def reset_game_stats(self):
        self.stats = GameStats()

    def is_game_over(self):
        return self.stats.game_status != 'game_active'

    def controller(self, key, pause_off):
        if key == KEYS['escape']:
            self.stats.is_exit = True
            endwin()
        elif key == KEYS['resize']:
            self.window.timeout(0)
            self.resize_game_win_handler(key)
            self.stats.is_restart = True
        elif key == KEYS['pause'] and not pause_off:
            self.pause()
        elif key == KEYS['restart']:
            self.stats.is_restart = True

    def pause(self):
        self.stats.is_pause = not self.stats.is_pause

        if self.stats.is_pause:
            self._show_pause_message()
            key = self.window.getch()

            while key != KEYS['pause']:
                self.wait_for_keypress()
                key = self.window.getch()

            self.stats.is_pause = not self.stats.is_pause

        self.window.timeout(150)

    def _show_pause_message(self):
        message = ' PAUSE '
        color = get_color_by_name('yellow_text_black_bg')

        x = (self.game_area.width // 2 + self.game_area.begin_x) - (len(message) // 2)
        y = self.game_area.height // 2 + self.game_box_sizes['begin_y']

        draw_message(y, x, self.game_area.box, message, color)

    def ask_for_restart(self):
        flash()
        self.show_game_status()
        sleep(1)

        message = f" {MESSAGES['play_again']} "

        x = (self.game_area.width // 2) - (len(message) // 2)
        y = self.game_area.height // 2

        draw_message(y, x, self.game_area.box, message, BLINK)

        self.wait_for_keypress()
        flushinp()
        key = self.window.getch()

        self.stats.is_restart = True if key == KEYS['space'] else False

    def update_state_in_db(self, stat, value):
        update_game_state(self.game_name, stat, value)

    def show_game_status(self, y=1, x=1):
        color_name = GAME_STATUSES[self.stats.game_status]['color']
        color = get_color_by_name(color_name)

        empty_line = ' ' * (self.game_status_area.width - BASE_OFFSET)

        for offset in range(self.game_status_area.height - BASE_OFFSET):
            new_y = y + offset
            draw_message(new_y, x, self.game_status_area.box, empty_line, color)

        message = GAME_STATUSES[self.stats.game_status]['text']
        middle_x = (self.game_status_area.width // 2) - len(message) // 2
        draw_message(y + 1, middle_x, self.game_status_area.box, message, color)

    def show_side_menu_tips(self, game_state=None, game_tips=None):
        y = x = 2

        for curr_tips in get_game_tips(game_state, game_tips):
            tips_type = curr_tips['name']
            tips = curr_tips['tips']
            color = curr_tips['color']

            if not tips:
                continue

            for description, key in tips.items():
                if y >= self.tips_area.height - 2:
                    return

                message = f'{key} - {description}'
                line_width = self.tips_area.width - (x * 2)
                clear_field_line(y, x, self.tips_area.box, line_width)
                draw_message(y, x, self.tips_area.box, message, color)
                y += 1

            if tips_type == 'state':
                y += 1

    def setup_game_stats(self):
        pass

    def setup_game_field(self):
        pass

    def start_new_game(self):
        pass
