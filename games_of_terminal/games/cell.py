class BaseCell:
    def __init__(self, field_box, coordinates):
        self.field_box = field_box
        self.coordinates = coordinates

        self.state = {}
        self.colors = {}

    def is_cursor_here(self):
        return 'cursor' in self.state['settings']

    def select(self):
        if 'cursor' not in self.state['settings']:
            self.state['settings'].append('cursor')
            self.set_background_color()

    def unselect(self):
        if 'cursor' in self.state['settings']:
            self.state['settings'].remove('cursor')
            self.set_background_color()

    def get_background_color(self):
        return self.state['background_color']

    def set_background_color(self):
        self._update_cell_color()

    def _update_cell_color(self):
        color = self.get_background_color()
        self.field_box.bkgd(' ', color)
        self.field_box.refresh()
