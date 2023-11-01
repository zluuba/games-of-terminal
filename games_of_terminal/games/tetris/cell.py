from games_of_terminal.games.cell import BaseCell
from time import sleep


class TetrisCell(BaseCell):
    def __init__(self, field_box, coordinates):
        super().__init__(field_box, coordinates)

        self.state = {
            'owner': 'free',            # free, falling_block, placed_block
            # 'settings': [],
        }

        self.colors = {
            'free': self.get_color_by_name('white_text_black_bg'),
            'falling_block': self.get_color_by_name('white_text_black_bg'),
            'placed_block': self.get_color_by_name('black_text_pastel_dirty_blue_bg'),
        }

    def is_free(self):
        return self.state['owner'] == 'free'

    @property
    def block_color(self):
        return self.colors['falling_block']

    @block_color.setter
    def block_color(self, color):
        self.colors['falling_block'] = color
        self.set_background_color()

    @property
    def owner(self):
        return self.state['owner']

    @owner.setter
    def owner(self, player):
        self.state['owner'] = player

    def set_background_color(self):
        color = self.colors[self.state['owner']]

        self.field_box.bkgd(' ', color)
        self.field_box.refresh()
