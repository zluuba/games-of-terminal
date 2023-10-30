class Field:
    def __init__(self, parent_window, height, width, begin_y, begin_x):
        self.height = height
        self.width = width
        self.begin_y = begin_y
        self.begin_x = begin_x
        self._get_border_coordinates()

        self.box = parent_window.subwin(
            self.height, self.width,
            self.begin_y, self.begin_x,
        )
        self.draw_borders()

    def _get_border_coordinates(self):
        self.top_border = self.begin_y - 1
        self.bottom_border = self.height - self.top_border - 1
        self.left_border = self.begin_x
        self.right_border = self.width - self.left_border - 1

    def draw_borders(self):
        self.box.border()
