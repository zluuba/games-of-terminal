from games_of_terminal.app_interface import InterfaceManager
from games_of_terminal.games.game_stats import GameStats
from games_of_terminal.constants import (
    MESSAGES, KEYS, GAME_STATUSES, SIDE_MENU_TIPS,
    BASE_OFFSET,
)
from games_of_terminal.database.database import (
    update_game_state
)
from games_of_terminal.field import Field

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
            self.reset_stats()

    def reset_game_area(self):
        self.game_area.box.erase()
        self.game_area = Field(self.window, *self.game_box_sizes.values())
        self.game_area.box.refresh()

    def reset_stats(self):
        self.stats = GameStats()

    def is_game_over(self):
        return self.stats.game_status != 'game_active'

    def controller(self, key, pause_off):
        if key == KEYS['escape']:
            self.stats.is_exit = True
            endwin()
        elif key == KEYS['pause'] and not pause_off:
            self.pause()
        elif key == KEYS['restart']:
            self.stats.is_restart = True

    def pause(self):
        self.stats.is_pause = not self.stats.is_pause
        self.wait_for_keypress()

        if self.stats.is_pause:
            self._show_pause_message()
            key = self.window.getch()

            while key != KEYS['pause']:
                self.wait_for_keypress()
                key = self.window.getch()

            self.stats.is_pause = not self.stats.is_pause

        self.window.timeout(150)
        return

    def _show_pause_message(self):
        message = ' PAUSE '
        color = self.get_color_by_name('yellow_text_black_bg')

        x = (self.game_area.width // 2 + self.game_area.begin_x) - (len(message) // 2)
        y = self.game_area.height // 2 + self.game_box_sizes['begin_y']

        self.draw_message(y, x, self.game_area.box, message, color)

    def show_game_status(self, y=1, x=1):
        color_name = GAME_STATUSES[self.stats.game_status]['color']
        color = self.get_color_by_name(color_name)

        empty_line = ' ' * (self.game_status_area.width - BASE_OFFSET)

        for offset in range(self.game_status_area.height - BASE_OFFSET):
            new_y = y + offset
            # fill game_status field background, excluding borders
            self.draw_message(new_y, x, self.game_status_area.box, empty_line, color)

        message = GAME_STATUSES[self.stats.game_status]['text']
        middle_x = (self.game_status_area.width // 2) - len(message) // 2
        self.draw_message(y + 1, middle_x, self.game_status_area.box, message, color)

    def draw_game_tips(self, tips):
        color = self.get_color_by_name('strong_pastel_purple_text_black_bg')
        y, x = 3 + len(SIDE_MENU_TIPS), 2
        self.draw_side_menu_tips(y, x, tips, color)

    def ask_for_restart(self):
        """ Draws a message in the center of the playing field
        that the user can restart the game,
        waiting for a response (space bar pressing)
        """

        flash()
        self.show_game_status()
        sleep(1)

        message = f" {MESSAGES['play_again']} "

        x = (self.game_area.width // 2) - (len(message) // 2)
        y = self.game_area.height // 2

        self.draw_message(y, x, self.game_area.box, message, BLINK)

        self.wait_for_keypress()
        flushinp()
        key = self.window.getch()

        self.stats.is_restart = True if key == KEYS['space'] else False

    def update_stat_in_db(self, stat, value):
        update_game_state(self.game_name, stat, value)
