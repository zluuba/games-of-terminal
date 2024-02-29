from games_of_terminal.database.database import get_game_settings
from games_of_terminal.utils import (
    get_color_by_name, draw_message,
    get_current_color_scheme_name,
)

from .constants import COLORS


class Cell:
    def __init__(self, field_box, coordinates, game_name):
        self.field_box = field_box
        self.coordinates = coordinates

        self.height, self.width = field_box.getmaxyx()

        self.state = {
            'status': 'closed',                 # open, closed
            'visibility': 'not_shown',          # shown, not_shown
            'inside': 'empty',                  # empty, bomb
            'bombs_around': 0,                  # <int>
            'background_color': 0,              # <int> | <str>
            'settings': [],                     # flag, cursor
        }

        settings = get_game_settings(game_name)
        color_schemes = settings['color_schemes']
        color_scheme_name = get_current_color_scheme_name(color_schemes)
        self.colors = COLORS[color_scheme_name]

    def is_open(self):
        return self.state['status'] == 'open'

    def open_cell(self):
        self.state['status'] = 'open'

    def is_showed(self):
        return self.state['visibility'] == 'shown'

    def show_cell(self):
        self.state['visibility'] = 'shown'

    def hide_cell(self):
        self.state['visibility'] = 'not_shown'

    def is_bomb(self):
        return self.state['inside'] == 'bomb'

    def set_bomb(self):
        self.state['inside'] = 'bomb'

    def have_flag(self):
        return 'flag' in self.state['settings']

    def set_flag(self):
        self.state['settings'].append('flag')

    def remove_flag(self):
        self.field_box.erase()
        self.state['settings'].remove('flag')

    def is_cursor_here(self):
        return 'cursor' in self.state['settings']

    def select(self):
        self.state['settings'].append('cursor')
        self.set_background_color()

    def unselect(self):
        if 'cursor' in self.state['settings']:
            self.state['settings'].remove('cursor')
            self.set_background_color()

    @property
    def bombs_around(self):
        return self.state['bombs_around']

    @bombs_around.setter
    def bombs_around(self, value):
        self.state['bombs_around'] = value

    def get_background_color(self):
        return self.state['background_color']

    def is_empty(self):
        return (not self.is_open() and
                not self.is_bomb() and
                not self.have_flag() and
                not self.is_showed())

    def set_background_color(self):
        if self.is_cursor_here() and not self.is_showed():
            color_name = self.colors['cursor']
        elif self.have_flag() and not self.is_open():
            color_name = self.colors['flag']
        elif self.is_bomb() and self.is_open():
            color_name = self.colors['bomb']
        elif not self.is_open():
            color_name = self.colors['closed']
        else:
            num_of_bombs = min(self.bombs_around, 4)
            color_name = self.colors[num_of_bombs]

        color = get_color_by_name(color_name)
        self.state['background_color'] = color
        self.update_cell_color()

    def update_cell_color(self):
        color = self.get_background_color()
        self.field_box.bkgd(' ', color)
        self.field_box.refresh()

    def show_cell_text(self):
        text = ''

        if self.have_flag():
            text = 'bomb?'
        elif self.is_bomb() and self.is_open():
            text = 'boom!'
        elif self.is_open():
            num_of_bombs = self.bombs_around

            if num_of_bombs:
                text = str(num_of_bombs)

        y = self.height // 2
        x = (self.width // 2) - (len(text) // 2)

        draw_message(y, x, self.field_box, text)
        self.set_background_color()

    def clear_cell(self):
        self.field_box.erase()
