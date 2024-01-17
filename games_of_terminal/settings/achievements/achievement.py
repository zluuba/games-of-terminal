from games_of_terminal.settings.achievements.constants import (
    COLORS, PICTURE_COLORS_COUNT, CELL_WIDTH,
    SELECTED_CELL_COLOR, ACHIEVEMENTS_IN_ROW,
)
from games_of_terminal.sub_window import SubWindow

from random import choice


class Achievement:
    def __init__(self, parent_window, number, height, width, achieve_data):
        self.number = number
        self.height = height
        self.width = width

        self.name = achieve_data['name']
        self.description = achieve_data['description']
        self.status = achieve_data['status']
        self.date_received = achieve_data['date_received']

        self.picture_colors = self.get_random_picture_colors()
        self.picture_frame_color = self.get_picture_frame_color()
        self.picture = self.get_random_picture()

        self.state = {
            'is_selected': False,
        }

        # self.start_y, self.start_x = coords
        # self.box = SubWindow(parent_window, self.height, self.width, self.start_y, self.start_x)

    @property
    def is_selected(self):
        return self.state['is_selected']

    @is_selected.setter
    def is_selected(self, value):
        self.state['is_selected'] = value

    @staticmethod
    def get_random_picture_colors():
        random_picture_colors = []

        while len(random_picture_colors) != PICTURE_COLORS_COUNT:
            new_color = choice(COLORS['pictures'])

            if new_color not in random_picture_colors:
                random_picture_colors.append(new_color)

        return random_picture_colors

    def get_picture_frame_color(self):
        frame_color = choice(COLORS['pictures'])

        while frame_color in self.picture_colors:
            frame_color = choice(COLORS['pictures'])

        return frame_color

    def get_random_picture(self):
        random_picture = []

        for y in range(self.height):
            for x in range(0, self.width, CELL_WIDTH):
                if self.is_it_picture_frame_coordinates(y, x):
                    cells = [self.picture_frame_color] * CELL_WIDTH
                else:
                    random_color = choice(self.picture_colors)
                    cells = [random_color] * CELL_WIDTH

                random_picture.extend(cells)

        return random_picture

    def is_it_picture_frame_coordinates(self, y, x):
        return ((y == 0) or (y == self.height - 1) or
                (x in (0, 1)) or (x in (self.width - 1, self.width - 2)))

    def get_picture_color_by_index(self, index):
        if self.is_selected:
            return SELECTED_CELL_COLOR

        color_dict = self.picture[index]
        return color_dict[self.status]
