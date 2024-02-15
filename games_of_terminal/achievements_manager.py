from games_of_terminal.constants import (
    DEFAULT_COLOR, BASE_OFFSET, ACH_BG_COLOR_NAME,
    ACH_FRAME_COLOR_NAME, ACH_NAME_COLOR_NAME,
)
from games_of_terminal.database.database import (
    get_all_achievements, unlock_achievement,
)
from games_of_terminal.utils import (
    draw_message, get_color_by_name,
)

from curses import A_BOLD
from time import sleep


class AchievementsManager:
    def __init__(self, class_object):
        self.class_object = class_object
        self.achievements = self.get_locked_achievements()

        self.ach_text = 'ACHIEVEMENT UNLOCKED'
        self.ach_text_color = DEFAULT_COLOR + A_BOLD

        self.bg_color = get_color_by_name(ACH_BG_COLOR_NAME)
        self.frame_color = get_color_by_name(ACH_FRAME_COLOR_NAME) + A_BOLD
        self.ach_name_color = get_color_by_name(ACH_NAME_COLOR_NAME) + A_BOLD

    def get_locked_achievements(self):
        all_achievements = get_all_achievements()
        game_achievements = all_achievements[self.class_object.game_name]

        return [achievement for achievement in game_achievements
                if achievement['status'] == 'locked']

    def get_begin_coordinates(self, height, width):
        y = (self.class_object.game_area.height // 2) - (height // 2)
        x = (self.class_object.game_area.width // 2) - (width // 2)

        return y, x

    def get_frame_height_and_width(self, achievement):
        # frame (2) + empty space (2) + lines of text (2)
        height = BASE_OFFSET * 3

        ach_name_width = len(achievement['name']) + (BASE_OFFSET * 2)
        ach_unlocked_text_width = len(self.ach_text) + (BASE_OFFSET * 2)
        width = max(ach_name_width, ach_unlocked_text_width)

        return height, width

    def check(self, set_pause=False):
        for achievement in self.achievements:
            if self.has_achievement_been_unlocked(achievement):
                self.unlock_achievement(achievement, set_pause)

    def unlock_achievement(self, achievement, set_pause):
        unlock_achievement(self.class_object.game_name, achievement['name'])
        self.notify_user(achievement, set_pause)
        self.achievements = self.get_locked_achievements()

    def notify_user(self, achievement, set_pause):
        self.draw_achievement_animation(achievement)
        self.class_object.draw_game_window()

        if set_pause:
            self.class_object.pause()

    def draw_achievement_animation(self, achievement):
        height, width = self.get_frame_height_and_width(achievement)
        y, x = self.get_begin_coordinates(height, width)

        self.draw_background(height, width, y, x)
        self.draw_achievement_unlocked_text()
        self.draw_achievement_name(achievement)
        self.draw_frame_animation(height, width, y, x)

    def draw_background(self, height, width, y, x):
        for col in range(height):
            for row in range(width):
                draw_message(y + col, x + row,
                             self.class_object.game_area.box,
                             ' ', self.bg_color)

    def draw_achievement_unlocked_text(self):
        y = (self.class_object.game_area.height // 2) - 1
        x = ((self.class_object.game_area.width // 2) -
             (len(self.ach_text) // 2))

        draw_message(y, x, self.class_object.game_area.box,
                     self.ach_text, self.ach_text_color)

    def draw_achievement_name(self, achievement):
        achievement_name = achievement['name']

        y = (self.class_object.game_area.height // 2)
        x = ((self.class_object.game_area.width // 2) -
             (len(achievement_name) // 2))

        draw_message(y, x, self.class_object.game_area.box,
                     achievement_name, self.ach_name_color)

    def draw_frame_animation_chunk(self, y, x, top_coords,
                                   bottom_coords, char):
        top_y, top_x = top_coords
        bottom_y, bottom_x = bottom_coords

        draw_message(y + top_y, x + top_x,
                     self.class_object.game_area.box,
                     char, self.frame_color)
        draw_message(y + bottom_y, x + bottom_x,
                     self.class_object.game_area.box,
                     char, self.frame_color)

    def draw_frame_animation(self, height, width, y, x):
        for char in (':', ' '):
            finish_coords = [height - 1, width - 1]
            top_coords, bottom_coords = [0, 0], [0, 0]

            while ((top_coords <= finish_coords) and
                   (bottom_coords <= finish_coords)):

                self.draw_frame_animation_chunk(
                    y, x, top_coords, bottom_coords, char,
                )
                sleep(0.03)

                if top_coords[1] < finish_coords[1]:
                    top_coords[1] += 1
                else:
                    top_coords[0] += 1

                if bottom_coords[0] < finish_coords[0]:
                    bottom_coords[0] += 1
                else:
                    bottom_coords[1] += 1

    def has_achievement_been_unlocked(self, achievement):
        pass
