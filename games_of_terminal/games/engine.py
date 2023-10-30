from games_of_terminal.app_interface import InterfaceManager
from games_of_terminal.constants import (
    MESSAGES, KEYS, GAME_STATUSES, SIDE_MENU_TIPS,
)

from curses import flushinp, A_BLINK as BLINK


class GameEngine(InterfaceManager):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.state = {
            'pause': False,
            'game_status': 'game_is_on',
        }

    @property
    def game_status(self):
        return self.state['game_status']

    @game_status.setter
    def game_status(self, status):
        self.state['game_status'] = status

    def _pause(self):
        self.state['pause'] = not self.state['pause']
        self.wait_for_keypress()

        if self.state['pause']:
            self._show_pause_message()
            key = self.window.getch()

            while key != KEYS['pause']:
                self.wait_for_keypress()
                key = self.window.getch()

        self.window.timeout(150)
        return

    def _show_pause_message(self):
        message = ' PAUSE '
        color = self.get_color_by_name('yellow_text_black_bg')

        x = (self.game_area.width // 2 + self.game_area.begin_x) - (len(message) // 2)
        y = self.game_area.height // 2 + self.game_box_sizes['begin_y']

        self.draw_message(y, x, self.game_area.box, message, color)

    def show_game_status(self, y=1, x=1):
        message = GAME_STATUSES[self.game_status]['text']
        color_name = GAME_STATUSES[self.game_status]['color']
        color = self.get_color_by_name(color_name)

        empty_line = ' ' * (self.game_status_area.width - 2)

        for offset in range(3):
            new_y = y + offset
            self.draw_message(new_y, x, self.game_status_area.box, empty_line, color)

        middle_x = (self.game_status_area.width // 2) - len(message) // 2
        self.draw_message(y + 1, middle_x, self.game_status_area.box, message, color)

    def draw_game_tips(self, tips):
        color = self.get_color_by_name('strong_pastel_purple_text_black_bg')
        y, x = 3 + len(SIDE_MENU_TIPS), 2
        self.draw_side_menu_tips(y, x, tips, color)

    def _is_restart(self):
        # TODO: add transparent background color func
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
