from games_of_terminal.settings.achievements.constants import (
    COLORS, PICTURE_COLORS_COUNT, CELL_WIDTH,
    SELECTED_CELL_COLOR_NAME, PICTURE_ELEMENT,
)
from games_of_terminal.utils import (
    draw_message, get_color_by_name,
)

from random import choice


class Achievement:
    def __init__(self, parent_window, number, height, width, achieve_data):
        self.window = parent_window
        self.number = number
        self.height = height
        self.width = width

        self.name = achieve_data['name']
        self.description = achieve_data['description']
        self.status = achieve_data['status']
        self.date_received = achieve_data['date_received']

        self.picture_colors = self.get_random_picture_colors()
        self.picture_frame_color = self.get_random_picture_frame_color()
        self.picture = self.get_random_picture()

        self.y = self.x = 0

        self.state = {
            'is_selected': False,
        }

    @property
    def is_selected(self):
        return self.state['is_selected']

    @is_selected.setter
    def is_selected(self, value):
        self.state['is_selected'] = value

    def update_coordinates(self, new_y, new_x):
        self.y = new_y
        self.x = new_x

    def show(self, start_y=None, start_x=None):
        start_y = self.y if start_y is None else start_y
        start_x = self.x if start_x is None else start_x

        end_y = self.height + start_y
        end_x = self.width + start_x

        picture_colors_generator = iter(self.picture)

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                colors = next(picture_colors_generator)

                if self.is_selected and self.is_it_picture_frame_coordinates(
                        y - start_y, x - start_x,
                ):
                    color_name = SELECTED_CELL_COLOR_NAME
                else:
                    color_name = colors[self.status]

                color = get_color_by_name(color_name)
                draw_message(y, x, self.window, PICTURE_ELEMENT, color)

    @staticmethod
    def get_random_picture_colors():
        random_picture_colors = []

        while len(random_picture_colors) != PICTURE_COLORS_COUNT:
            new_color = choice(COLORS['pictures'])

            if new_color not in random_picture_colors:
                random_picture_colors.append(new_color)

        return random_picture_colors

    def get_random_picture_frame_color(self):
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
        start_y = start_x = 0
        end_y = self.height - 1
        end_x = self.width - 1

        return ((y == start_y) or
                (y == end_y) or
                (x in (start_x, start_x + 1)) or
                (x in (end_x, end_x - 1)))
