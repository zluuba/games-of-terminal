from games_of_terminal.app_interface import InterfaceManager
from games_of_terminal.constants import (
    MESSAGES, KEYS, GAME_STATUSES,
)
import curses


class GameEngine(InterfaceManager):
    def __init__(self, canvas):
        super().__init__(canvas)
        self._setup_side_menu()

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

        x = (self.game_box_width // 2 + self.game_box_sizes['begin_x']) - (len(message) // 2)
        y = self.game_box_height // 2 + self.game_box_sizes['begin_y']

        self.draw_message(y, x, self.game_box, message, color)

    def _show_game_result_message(self):
        message = GAME_STATUSES[self.game_status]['text']
        color_name = GAME_STATUSES[self.game_status]['color']
        color = self.get_color_by_name(color_name)

        y, x = self.side_menu_box_height - 2, 1
        empty_line = ' ' * (self.side_menu_box_width - 2)

        for offset in range(0, -3, -1):
            new_y = y + offset
            self.draw_message(new_y, x, self.side_menu_box, empty_line, color)

        middle_x = (self.side_menu_box_width // 2) - len(message) // 2
        self.draw_message(y - 1, middle_x, self.side_menu_box, message, color)

    def _is_restart(self):
        # TODO: add transparent background color func
        """ Draws a message in the center of the playing field
        that the user can restart the game,
        waiting for a response (space bar pressing)
        """

        message = f" {MESSAGES['play_again']} "

        x = (self.game_box_width // 2) - (len(message) // 2)
        y = self.game_box_height // 2

        self.draw_message(y, x, self.game_box, message, curses.A_BLINK)

        self.wait_for_keypress()
        curses.flushinp()
        key = self.window.getch()

        if key == KEYS['space']:
            self.game_box.erase()
            return True
        return False
