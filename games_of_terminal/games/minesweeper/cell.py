from games_of_terminal.utils import get_color_by_name, draw_message


class Cell:
    def __init__(self, field_box, coordinates):
        self.field_box = field_box
        self.coordinates = coordinates

        height, width = field_box.getmaxyx()
        self.center_y, self.center_x = height // 2, width // 2

        self.state = {
            'status': 'closed',                 # open, closed
            'visibility': 'not_shown',          # shown, not_shown
            'inside': 'empty',                  # empty, bomb
            'bombs_around': 0,                  # <int>
            'background_color': 0,              # <int> | <str>
            'settings': [],                     # flag, cursor
        }

        self.colors = {
            0: get_color_by_name('white_text_pastel_blue_bg'),
            1: get_color_by_name('white_text_light_blue_bg'),
            2: get_color_by_name('white_text_medium_blue_bg'),
            3: get_color_by_name('white_text_dark_medium_blue_bg'),
            4: get_color_by_name('white_text_deep_blue_bg'),

            'bomb': get_color_by_name('white_text_red_bg'),
            'closed': get_color_by_name('white_text_black_bg'),
            'cursor': get_color_by_name('white_text_light_grey_bg'),
            'flag': get_color_by_name('white_text_deep_purple_bg'),
        }

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

    def bombs_around(self):
        return self.state['bombs_around']

    def set_bombs_around_number(self, number):
        self.state['bombs_around'] = number

    def get_background_color(self):
        return self.state['background_color']

    def is_empty(self):
        return (not self.is_open() and
                not self.is_bomb() and
                not self.have_flag() and
                not self.is_showed())

    def set_background_color(self):
        if self.is_cursor_here() and not self.is_showed():
            color = self.colors['cursor']
        elif self.have_flag() and not self.is_open():
            color = self.colors['flag']
        elif self.is_bomb() and self.is_open():
            color = self.colors['bomb']
        elif not self.is_open():
            color = self.colors['closed']
        else:
            num_of_bombs = min(self.bombs_around(), 4)
            color = self.colors[num_of_bombs]

        self.state['background_color'] = color
        self.update_cell_color()

    def update_cell_color(self):
        color = self.get_background_color()
        self.field_box.bkgd(' ', color)
        self.field_box.refresh()

    def show_cell_text(self, text=''):
        if self.have_flag():
            text = 'bomb?'
        elif self.is_bomb() and self.is_open():
            text = 'boom!'
        elif self.is_open():
            num_of_bombs = self.bombs_around()

            if num_of_bombs:
                text = str(num_of_bombs)

        y = self.center_y
        x = self.center_x - (len(text) // 2)

        draw_message(y, x, self.field_box, text)
        self.set_background_color()
