from curses import window as curses_window
from typing import Optional


class SubWindow:
    def __init__(self, parent_window: curses_window,
                 height: int, width: int,
                 begin_y: int, begin_x: int,
                 show_borders: Optional[bool] = True) -> None:

        self.height = height
        self.width = width
        self.begin_y = begin_y
        self.begin_x = begin_x
        self.set_border_coordinates()

        self.box = parent_window.subwin(
            self.height, self.width,
            self.begin_y, self.begin_x,
        )

        if show_borders:
            self.show_borders()

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}>'

    def set_border_coordinates(self):
        self.top_border = self.begin_y - 1
        self.bottom_border = self.height - self.top_border - 1
        self.left_border = self.begin_x
        self.right_border = self.width - self.left_border - 1

    def show_borders(self):
        self.box.border()
