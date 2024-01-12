from games_of_terminal.settings.achievements.constants import COLORS

from random import choice


class Achievement:
    def __init__(self, height, width, **kwargs):
        self.height = height
        self.width = width

        self.name = kwargs['name']
        self.description = kwargs['description']
        self.status = kwargs['status']
        self.date_received = kwargs['date_received']

        self.picture_colors_num = 3
        self.picture_colors = self.get_random_picture_colors()
        self.picture = self.get_random_picture()

    def get_random_picture_colors(self):
        random_picture_colors = []

        while len(random_picture_colors) != self.picture_colors_num:
            new_color = choice(COLORS)

            if new_color not in random_picture_colors:
                random_picture_colors.append(new_color)

        return random_picture_colors

    def get_random_picture(self):
        random_picture = []

        for _ in range(self.height * self.width):
            random_color = choice(self.picture_colors)
            random_picture.append(random_color)

        return random_picture
