from games_of_terminal.database.database import get_game_settings
from games_of_terminal.games.cell import BaseCell
from games_of_terminal.utils import (
    get_color_by_name, get_current_color_scheme_name,
)

from .constants import COLORS

from time import sleep


class TicTacToeCell(BaseCell):
    def __init__(self, field_box, coordinates, game_name):
        super().__init__(field_box, coordinates)
        self.game_name = game_name

        self.state = {
            'owner': 'free',            # free, user, computer
            'field_number': 0,
            'settings': [],             # cursor
        }

        self.set_color_scheme()

    def is_free(self):
        return self.state['owner'] == 'free'

    @property
    def owner(self):
        return self.state['owner']

    @owner.setter
    def owner(self, player):
        self.state['owner'] = player

        self.flash()
        self.set_background_color()

    @property
    def field_number(self):
        return self.state['field_number']

    @field_number.setter
    def field_number(self, number):
        self.state['field_number'] = number

    def set_background_color(self):
        color_name = self.colors[self.state['owner']]

        if self.is_cursor_here():
            color_name = self.colors['cursor']

        color = get_color_by_name(color_name)
        self.field_box.bkgd(' ', color)
        self.field_box.refresh()

    def flash(self):
        cell_color_name = self.colors[self.state['owner']]
        cell_color = get_color_by_name(cell_color_name)

        self.field_box.bkgd(' ', cell_color)
        self.field_box.refresh()

        sleep(0.2)
        self.set_background_color()

    def set_color_scheme(self):
        settings = get_game_settings(self.game_name)
        color_schemes = settings['color_schemes']
        color_scheme_name = get_current_color_scheme_name(color_schemes)
        self.colors = COLORS[color_scheme_name]
