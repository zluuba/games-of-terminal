from games_of_terminal.app_interface import InterfaceManager
from games_of_terminal.constants import (
    MESSAGES, KEYS, GAME_STATUSES, SIDE_MENU_TIPS,
    BASE_OFFSET,
)

from curses import flash, flushinp, endwin, A_BLINK as BLINK
from time import sleep


class GameEngine(InterfaceManager):
    def __init__(self, canvas, game_name):
        super().__init__(canvas)

        self.state = {
            'game_name': game_name,
            'game_status': 'game_active',
            'pause': False,
            'exit': False,
        }

    @property
    def game_name(self):
        return self.state['game_name']

    @property
    def game_status(self):
        return self.state['game_status']

    @game_status.setter
    def game_status(self, status):
        self.state['game_status'] = status

    @property
    def is_exit(self):
        return self.state['exit']

    @is_exit.setter
    def is_exit(self, value):
        self.state['exit'] = value

    def is_game_over(self):
        return self.game_status != 'game_active'

    def controller(self, key, pause_off):
        if key == KEYS['escape']:
            self.is_exit = True
            endwin()
        elif key == KEYS['pause'] and not pause_off:
            self.pause()
        elif key == KEYS['restart']:
            self.game_area.box.erase()
            self.__init__(self.canvas, self.game_name)
            self.start_new_game()

    def pause(self):
        self.state['pause'] = not self.state['pause']
        self.wait_for_keypress()

        if self.state['pause']:
            self._show_pause_message()
            key = self.window.getch()

            while key != KEYS['pause']:
                self.wait_for_keypress()
                key = self.window.getch()

            self.state['pause'] = not self.state['pause']

        self.window.timeout(150)
        return

    def _show_pause_message(self):
        message = ' PAUSE '
        color = self.get_color_by_name('yellow_text_black_bg')

        x = (self.game_area.width // 2 + self.game_area.begin_x) - (len(message) // 2)
        y = self.game_area.height // 2 + self.game_box_sizes['begin_y']

        self.draw_message(y, x, self.game_area.box, message, color)

    def show_game_status(self, y=1, x=1):
        color_name = GAME_STATUSES[self.game_status]['color']
        color = self.get_color_by_name(color_name)

        empty_line = ' ' * (self.game_status_area.width - BASE_OFFSET)

        for offset in range(self.game_status_area.height - BASE_OFFSET):
            new_y = y + offset
            # fill game_status field background, excluding borders
            self.draw_message(new_y, x, self.game_status_area.box, empty_line, color)

        message = GAME_STATUSES[self.game_status]['text']
        middle_x = (self.game_status_area.width // 2) - len(message) // 2
        self.draw_message(y + 1, middle_x, self.game_status_area.box, message, color)

    def draw_game_tips(self, tips):
        color = self.get_color_by_name('strong_pastel_purple_text_black_bg')
        y, x = 3 + len(SIDE_MENU_TIPS), 2
        self.draw_side_menu_tips(y, x, tips, color)

    def ask_for_restart(self):
        flash()
        self.show_game_status()
        sleep(1)

        if self._is_restart():
            self.__init__(self.canvas, self.game_name)
            self.start_new_game()
        return False

    def _is_restart(self):
        """ Draws a message in the center of the playing field
        that the user can restart the game,
        waiting for a response (space bar pressing)
        """

        message = f" {MESSAGES['play_again']} "

        x = (self.game_area.width // 2) - (len(message) // 2)
        y = self.game_area.height // 2

        self.draw_message(y, x, self.game_area.box, message, BLINK)

        self.wait_for_keypress()
        flushinp()
        key = self.window.getch()

        if key == KEYS['space']:
            self.game_area.box.erase()
            return True
        return False
