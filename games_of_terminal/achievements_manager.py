from games_of_terminal.constants import (
    ACHIEVEMENT_WIN_HEIGHT, FRAME_CHARS,
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

        self.y, self.x = self.get_begin_coordinates()
        self.frame_color = get_color_by_name('strong_red_text_black_bg')

    def get_locked_achievements(self):
        all_achievements = get_all_achievements()
        locked_achievements = []

        for game_name, achievements in all_achievements.items():
            if self.class_object.game_name != game_name:
                continue

            for achievement in achievements:
                if achievement['status'] == 'locked':
                    locked_achievements.append(achievement)

        return locked_achievements

    def get_begin_coordinates(self):
        y = (self.class_object.game_area.height // 2) - (4 // 2) - 1
        x = (self.class_object.game_area.width // 2) - (26 // 2)

        return y, x

    def check(self, set_pause=False):
        for achievement in self.achievements:
            if self.has_achievement_been_unlocked(achievement):
                self.unlock_achievement(achievement, set_pause)

    def unlock_achievement(self, achievement, set_pause):
        unlock_achievement(self.class_object.game_name, achievement['name'])
        self.notify_user(achievement, set_pause)
        self.achievements = self.get_locked_achievements()

    def notify_user(self, achievement, set_pause):
        pass

    def has_achievement_been_unlocked(self, achievement):
        pass

    def draw_achievement_unlocked_text(self):
        text = 'ACHIEVEMENT UNLOCKED'
        color = get_color_by_name('light_grey_text_black_bg') + A_BOLD

        y = (self.class_object.game_area.height // 2) - 1
        x = (self.class_object.game_area.width // 2) - (len(text) // 2)

        draw_message(y, x, self.class_object.game_area.box, text, color)

    def draw_achievement_name(self, achievement):
        achievement_name = achievement['name']
        color = get_color_by_name('bright_white_text_black_bg') + A_BOLD

        y = (self.class_object.game_area.height // 2)
        x = (self.class_object.game_area.width // 2) - (len(achievement_name) // 2)

        draw_message(y, x, self.class_object.game_area.box, achievement_name, color)

    def draw_background(self):
        bg_color = get_color_by_name('light_grey_text_black_bg')
        y = (self.class_object.game_area.height // 2) - (4 // 2) - 1
        x = (self.class_object.game_area.width // 2) - (26 // 2)

        for col in range(6):
            for row in range(27):
                draw_message(y + col, x + row,
                             self.class_object.game_area.box, ' ', bg_color)

    def draw_frame_animation_chunk(self, char, j, k):
        draw_message(self.y + j[0], self.x + j[1],
                     self.class_object.game_area.box,
                     char, self.frame_color)
        draw_message(self.y + k[0], self.x + k[1],
                     self.class_object.game_area.box,
                     char, self.frame_color)

    def draw_frame_animation(self, action):
        char = FRAME_CHARS[action]
        finish, j, k = [5, 26], [0, 0], [0, 0]

        while (k <= finish) and (j <= finish):
            self.draw_frame_animation_chunk(char, j, k)
            sleep(0.025)

            if j[1] < finish[1]:
                j[1] += 1
            else:
                j[0] += 1

            if k[0] < finish[0]:
                k[0] += 1
            else:
                k[1] += 1

        sleep(0.1)
