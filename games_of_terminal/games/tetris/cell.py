from games_of_terminal.games.cell import BaseCell
from time import sleep


class TetrisCell(BaseCell):
    def __init__(self, field_box, coordinates):
        super().__init__(field_box, coordinates)

        self.state = {
            'owner': 'free',            # free, block, placed_block
            'settings': [],             # hide
        }

        self.colors = {
            'free': self.get_color_by_name('white_text_black_bg'),
            'placed_block': self.get_color_by_name('black_text_pastel_dirty_blue_bg'),
            'I-block': self.get_color_by_name('white_text_pastel_blue_bg'),
            'J-block': self.get_color_by_name('white_text_green_bg'),
            'L-block': self.get_color_by_name('white_text_deep_blue_bg'),
            'O-block': self.get_color_by_name('white_text_pink_bg'),
            'Z-block': self.get_color_by_name('white_text_yellow_bg'),
            'T-block': self.get_color_by_name('black_text_deep_pink_bg'),
            'S-block': self.get_color_by_name('white_text_light_purple_bg'),
        }

    def is_free(self):
        return self.owner == 'free'

    def set_free(self):
        self.owner = 'free'

    @property
    def color(self):
        return self.colors[self.owner]

    @color.setter
    def color(self, color):
        self.colors[self.owner] = color
        self.colorize()

    @property
    def owner(self):
        return self.state['owner']

    @owner.setter
    def owner(self, new_owner):
        self.state['owner'] = new_owner

    def colorize(self):
        color = self.colors[self.state['owner']]

        self.field_box.bkgd(' ', color)
        self.field_box.refresh()
