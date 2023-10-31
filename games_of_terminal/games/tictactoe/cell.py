from games_of_terminal.games.cell import BaseCell
from time import sleep


class TicTacToeCell(BaseCell):
    def __init__(self, field_box, coordinates):
        super().__init__(field_box, coordinates)

        self.field_box = field_box
        self.coordinates = coordinates

        self.state = {
            'owner': 'free',            # free, user, computer
            'field_number': 0,
            'settings': [],             # cursor
        }

        self.colors = {
            'free': self.get_color_by_name('white_text_dark_grey_bg'),
            'cursor': self.get_color_by_name('white_text_light_grey_bg'),
            'user': self.get_color_by_name('black_text_deep_pink_bg'),
            'computer': self.get_color_by_name('black_text_pastel_dirty_blue_bg'),
        }

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
        color = self.colors[self.state['owner']]

        if self.is_cursor_here():
            color = self.colors['cursor']

        self.field_box.bkgd(' ', color)
        self.field_box.refresh()

    def flash(self):
        cell_color = self.colors[self.state['owner']]

        self.field_box.bkgd(' ', cell_color)
        self.field_box.refresh()

        sleep(0.2)
        self.set_background_color()
