class Field:
    def __init__(self, parent_window, height, width, begin_y, begin_x):
        self.height = height
        self.width = width
        self.begin_y = begin_y
        self.begin_x = begin_x

        self.box = parent_window.subwin(
            self.height, self.width,
            self.begin_y, self.begin_x,
        )
        self.draw_borders()

    def draw_borders(self):
        self.box.border()
