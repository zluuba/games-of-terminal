from games_of_terminal.games.constants import (
    MESSAGES, KEYS, LOGO_GOT, APP_NAME,
)
from games_of_terminal.games.colors import Colors
import curses


class Engine(Colors):
    def __init__(self, canvas):
        super().__init__()

        self.canvas = canvas
        self._setup()

    def _setup(self):
        self.height, self.width = self.canvas.getmaxyx()

        # TODO: add ability to change themes - black/white (?)
        canvas_bg_color = self.get_color_by_name('white_text_black_bg')
        self.canvas.bkgd(' ', canvas_bg_color)

        self._setup_sizes()
        self._draw_window()
        self._setup_boxes()

    def _draw_window(self):
        sizes = self.window_box_sizes.values()
        self.window = curses.newwin(*sizes)
        self.window.nodelay(True)
        self.window.keypad(True)

    def _draw_box(self, sizes):
        box = self.window.subwin(*sizes.values())
        box.border()
        return box

    def _setup_boxes(self):
        self.game_box = self._draw_box(self.game_box_sizes)
        self.game_box_height, self.game_box_width = self.game_box.getmaxyx()

        self.side_menu_box = self._draw_box(self.side_menu_box_sizes)
        self.side_menu_box_height, self.side_menu_box_width = self.side_menu_box.getmaxyx()

        self.logo_box = self._draw_box(self.logo_box_sizes)
        self.logo_box_height, self.logo_box_width = self.logo_box.getmaxyx()

    def _setup_sizes(self):
        self.window_box_sizes = {
            'lines': self.height,
            'cols': self.width,
            'begin_y': 0,
            'begin_x': 0,
        }

        self.game_box_sizes = {
            'lines': self.height - 2,
            'cols': self.width - 27,
            'begin_y': 1,
            'begin_x': 0,
        }

        self.side_menu_box_sizes = {
            'lines': self.height - 8,
            'cols': 27,
            'begin_y': 7,
            'begin_x': self.width - 27,
        }

        self.logo_box_sizes = {
            'lines': 7,
            'cols': 27,
            'begin_y': 1,
            'begin_x': self.width - 27,
        }


class GameEngine(Engine):
    def __init__(self, canvas):
        super().__init__(canvas)
        self._setup_side_menu()

        self.state = {
            'pause': False,
            'game_status': 'game_is_on',
        }

        self.statuses = {
            'user_win': {'text': 'You WIN!', 'color': 'white_text_green_bg'},
            'user_lose': {'text': 'You LOSE', 'color': 'white_text_red_bg'},
            'tie': {'text': 'TIE', 'color': 'white_text_pink_bg'},
        }

    def _setup_side_menu(self):
        self._draw_logo()
        # self._draw_tips

    def _draw_logo(self):
        color = self.get_color_by_name('white_text_black_bg')

        for y, line in enumerate(LOGO_GOT, start=1):
            self._draw_message(y, 2, self.logo_box, line, color)

        y, x = 6, (self.logo_box_width - len(APP_NAME)) // 2
        self._draw_message(y, x, self.logo_box, APP_NAME, color)

    @property
    def game_status(self):
        # TODO: rebuild props - create 'is_user_win' func ?
        return self.state['game_status']

    @game_status.setter
    def game_status(self, status):
        self.state['game_status'] = status

    def _pause(self):
        self.state['pause'] = not self.state['pause']
        self._wait()

        if self.state['pause']:
            self._show_pause_message()
            key = self.window.getch()

            while key != KEYS['pause']:
                self._wait()
                key = self.window.getch()

        self.window.timeout(150)
        return

    def _show_pause_message(self):
        message = ' PAUSE '
        color = self.get_color_by_name('yellow_text_black_bg')

        x = (self.game_box_width // 2 + self.game_box_sizes['begin_x']) - (len(message) // 2)
        y = self.game_box_height // 2 + self.game_box_sizes['begin_y']

        self._draw_message(y, x, self.game_box, message, color)

    def _show_who_won(self):
        message = self.statuses[self.game_status]['text']
        color_name = self.statuses[self.game_status]['color']
        color = self.get_color_by_name(color_name)

        y, x = self.side_menu_box_height - 2, 1
        empty_line = ' ' * (self.side_menu_box_width - 2)

        for offset in range(0, -3, -1):
            new_y = y + offset
            self._draw_message(new_y, x, self.side_menu_box, empty_line, color)

        middle_x = (self.side_menu_box_width // 2) - len(message) // 2
        self._draw_message(y - 1, middle_x, self.side_menu_box, message, color)

    def _is_restart(self):
        # TODO: add transparent background color func
        """ Draws a message in the center of the playing field
        that the user can restart the game,
        waiting for a response (space bar pressing)
        """

        message = f" {MESSAGES['play_again']} "

        x = (self.game_box_width // 2) - (len(message) // 2)
        y = self.game_box_height // 2

        self._draw_message(y, x, self.game_box, message, curses.A_BLINK)

        self._wait()
        curses.flushinp()
        key = self.window.getch()

        if key == KEYS['space']:
            self.game_box.erase()
            return True
        return False

    @staticmethod
    def _draw_message(y, x, field, message, color):
        field.addstr(y, x, message, color)
        field.refresh()

    @staticmethod
    def _hide_cursor():
        curses.curs_set(0)

    def _wait(self):
        self.window.timeout(-1)
