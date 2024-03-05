from games_of_terminal.constants import (
    DEFAULT_COLOR, BASE_OFFSET, ACH_BG_COLOR_NAME,
    ACH_FRAME_COLOR_NAME, ACH_NAME_COLOR_NAME, ACH_TEXT,
)
from games_of_terminal.database.database import (
    get_all_achievements, unlock_achievement,
)
from games_of_terminal.games.achievements_manager import (
    GlobalAchievementsManager,
)
from games_of_terminal.utils import (
    draw_message, get_color_by_name,
)

from curses import A_BOLD as BOLD
from time import sleep


class AchievementsManager:
    def __init__(self, class_object, in_game=True):
        self.class_object = class_object

        if in_game:
            self.window = self.class_object.game_area
            self.box = self.class_object.game_area.box
        else:
            self.window = self.class_object
            self.box = self.class_object.window

        self.achievements = self.get_locked_achievements()
        self.global_achievements = self.get_global_achievements()
        self.global_achievements_manager = GlobalAchievementsManager()

        self.bg_color = get_color_by_name(ACH_BG_COLOR_NAME)
        self.frame_color = get_color_by_name(ACH_FRAME_COLOR_NAME) + BOLD
        self.ach_name_color = get_color_by_name(ACH_NAME_COLOR_NAME) + BOLD
        self.ach_text_color = DEFAULT_COLOR + BOLD

    def get_locked_achievements(self):
        all_achievements = get_all_achievements()

        if not hasattr(self.class_object, 'game_name'):
            return []

        game_achievements = all_achievements[self.class_object.game_name]

        return [achievement for achievement in game_achievements
                if achievement['status'] == 'locked']

    @staticmethod
    def get_global_achievements():
        all_achievements = get_all_achievements()
        global_achievements = all_achievements['Global']

        return [achievement for achievement in global_achievements
                if achievement['status'] == 'locked']

    def get_begin_coordinates(self, height, width):
        y = (self.window.height // 2) - (height // 2)
        x = (self.window.width // 2) - (width // 2)

        return y, x

    @staticmethod
    def get_frame_height_and_width(achievement):
        # frame (2) + offsets (2) + lines of text (2)
        height = BASE_OFFSET * 3

        ach_name_width = len(achievement['name']) + (BASE_OFFSET * 2)
        ach_unlocked_text_width = len(ACH_TEXT) + (BASE_OFFSET * 2)
        width = max(ach_name_width, ach_unlocked_text_width)

        return height, width

    def check(self, set_pause=False, **kwargs):
        self.check_local_achievements(set_pause, **kwargs)
        self.check_global_achievements(set_pause, **kwargs)

    def check_local_achievements(self, set_pause=False, **kwargs):
        for achievement in self.achievements:
            if self.has_achievement_been_unlocked(achievement, **kwargs):
                self.unlock_achievement(achievement, set_pause)

    def check_global_achievements(self, set_pause=False, **kwargs):
        for achievement in self.global_achievements:
            if self.global_achievements_manager.has_achievement_been_unlocked(
                    achievement, **kwargs,
            ):
                self.unlock_achievement(achievement, set_pause, 'Global')

    def unlock_achievement(self, achievement, set_pause, game_name=None):
        if game_name is None:
            game_name = self.class_object.game_name

        unlock_achievement(game_name, achievement['name'])
        self.achievements = self.get_locked_achievements()

        self.notify_user(achievement, set_pause)

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
                draw_message(y + col, x + row, self.box, ' ', self.bg_color)

    def draw_achievement_unlocked_text(self):
        y = (self.window.height // 2) - 1
        x = (self.window.width // 2) - (len(ACH_TEXT) // 2)

        draw_message(y, x, self.box, ACH_TEXT, self.ach_text_color)

    def draw_achievement_name(self, achievement):
        achievement_name = achievement['name']

        y = (self.window.height // 2)
        x = ((self.window.width // 2) -
             (len(achievement_name) // 2))

        draw_message(y, x, self.box,
                     achievement_name, self.ach_name_color)

    def draw_frame_animation_chunk(self, y, x, top_coords,
                                   bottom_coords, char):
        top_y, top_x = top_coords
        bottom_y, bottom_x = bottom_coords

        draw_message(y + top_y, x + top_x,
                     self.box, char, self.frame_color)
        draw_message(y + bottom_y, x + bottom_x,
                     self.box, char, self.frame_color)

    def draw_frame_animation(self, height, width, y, x):
        for char in (':', ' '):
            finish_coords = [height - 1, width - 1]
            top_coords, bottom_coords = [0, 0], [0, 0]

            while top_coords <= finish_coords:
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

    def has_achievement_been_unlocked(self, achievement, **kwargs):
        pass
