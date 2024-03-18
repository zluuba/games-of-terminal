from games_of_terminal.constants import (
    MESSAGES, KEYS, GAME_STATUSES, BASE_OFFSET,
)
from games_of_terminal.database.database import (
    get_game_settings, get_game_stat_value,
)
from games_of_terminal.interface_manager import InterfaceManager
from games_of_terminal.games.game_stats import GameStats
from games_of_terminal.settings.all_settings.core import GamesSettings
from games_of_terminal.sub_window import SubWindow
from games_of_terminal.log import log
from games_of_terminal.utils import (
    get_side_menu_tips, draw_message,
    clear_field_line, get_color_by_name,
    is_current_setting_option_is_default,
)

from curses import flash, flushinp, endwin, A_BLINK as BLINK
from time import sleep


class GameEngine(InterfaceManager):
    @log
    def __init__(self, canvas, game_name):
        super().__init__(canvas)

        self.game_name = game_name
        self.stats = GameStats()

    @log
    def run(self):
        while True:
            self.setup_game_stats()
            self.setup_game_field()
            self.start_new_game()

            if self.stats.is_exit or not self.stats.is_restart:
                break

            self.reset_game_stats()
            self.reset_game_area()

    @log
    def reset_game_stats(self):
        self.stats = GameStats()

    @log
    def reset_game_area(self):
        self.game_area.box.erase()
        self.game_area = SubWindow(self.window, *self.game_box_sizes.values())
        self.game_area.box.refresh()

    def is_game_over(self):
        return self.stats.game_status != 'game_active'

    def controller(self, key, pause_on):
        if key == KEYS['escape']:
            self.stats.is_exit = True
            endwin()
        elif key == KEYS['resize']:
            self.window.timeout(0)
            self.resize_game_win_handler(key)
            self.stats.is_restart = True
        elif key == KEYS['pause'] and pause_on:
            self.pause()
        elif key == KEYS['restart']:
            self.stats.is_restart = True
        elif key == KEYS['settings']:
            self.open_game_settings()

    @log
    def pause(self):
        self.stats.is_pause = not self.stats.is_pause

        if self.stats.is_pause:
            self.show_pause_message()

            while True:
                key = self.window.getch()
                self.wait_for_keypress()

                if key == KEYS['escape']:
                    self.stats.is_exit = True
                    return
                elif key == KEYS['settings']:
                    self.open_game_settings()
                    self.show_pause_message()
                elif key == KEYS['pause']:
                    break

            self.stats.is_pause = not self.stats.is_pause
            self.draw_game_window()

        self.window.timeout(150)

    def show_pause_message(self):
        message = f" {MESSAGES['pause']} "
        color = get_color_by_name('yellow_text_black_bg')

        x = ((self.game_area.width // 2 + self.game_area.begin_x) -
             (len(message) // 2))
        y = self.game_area.height // 2 + self.game_box_sizes['begin_y']

        draw_message(y, x, self.game_area.box, message, color)

    @log
    def ask_for_restart(self):
        flash()
        self.show_game_status()
        sleep(0.5)

        message = f" {MESSAGES['play_again']} "

        x = (self.game_area.width // 2) - (len(message) // 2)
        y = self.game_area.height // 2

        draw_message(y, x, self.game_area.box, message, BLINK)

        self.wait_for_keypress()
        flushinp()
        key = self.window.getch()

        self.stats.is_restart = True if key == KEYS['space'] else False

    def show_game_status(self, y=1, x=1):
        color_name = GAME_STATUSES[self.stats.game_status]['color']
        color = get_color_by_name(color_name)

        empty_line = ' ' * (self.game_status_area.width - BASE_OFFSET)

        for offset in range(self.game_status_area.height - BASE_OFFSET):
            new_y = y + offset
            draw_message(
                new_y, x, self.game_status_area.box, empty_line, color
            )

        message = GAME_STATUSES[self.stats.game_status]['text']
        middle_x = (self.game_status_area.width // 2) - len(message) // 2
        draw_message(
            y + 1, middle_x, self.game_status_area.box, message, color
        )

    def show_side_menu_tips(self, game_state=None, game_tips=None):
        side_menu_tips = get_side_menu_tips(game_state, game_tips)
        y = x = 2

        for curr_tips in side_menu_tips:
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

    def open_game_settings(self):
        self.window.erase()
        settings = GamesSettings(self.canvas, self.game_name,
                                 in_game_mode=True)
        settings.run()

        self.draw_game_window()

    def show_all_areas_borders(self):
        self.game_area.show_borders()
        self.logo_area.show_borders()
        self.tips_area.show_borders()
        self.game_status_area.show_borders()

    def is_settings_option_was_change(self, option):
        settings = get_game_settings(self.game_name)
        color_schemes = settings[option]

        return not is_current_setting_option_is_default(color_schemes)

    def set_best_score(self):
        data = get_game_stat_value(self.game_name, 'best_score')
        self.stats.best_score = int(data)

    def draw_game_window(self):
        pass

    def setup_game_stats(self):
        pass

    def setup_game_field(self):
        pass

    def start_new_game(self):
        pass
