from games_of_terminal.settings.achievements.constants import COLORS

from random import choice


class Achievement:
    def __init__(self, height, width, achieve_data):
        self.height = height
        self.width = width

        self.name = achieve_data['name']
        self.description = achieve_data['description']
        self.status = achieve_data['status']
        self.date_received = achieve_data['date_received']

        self.fake_status = choice(['locked', 'unlocked'])

        self.picture_colors_num = 3
        self.picture_colors = self.get_random_picture_colors()
        self.picture_frame_color = self.get_picture_frame_color()
        self.picture = self.get_random_picture()

    def get_random_picture_colors(self):
        random_picture_colors = []

        while len(random_picture_colors) != self.picture_colors_num:
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
            for x in range(0, self.width, 2):
                if (y == 0) or (y == self.height - 1):
                    random_picture.extend([self.picture_frame_color] * 2)
                    continue
                if (x in (0, 1)) or (x in (self.width - 1, self.width - 2)):
                    random_picture.extend([self.picture_frame_color] * 2)
                    continue

                random_color = choice(self.picture_colors)
                random_picture.extend([random_color] * 2)

        return random_picture

    def get_picture_color_by_index(self, index):
        color_dict = self.picture[index]
        return color_dict[self.fake_status]
