from games_of_terminal.constants import KEYS, DEFAULT_COLOR
from games_of_terminal.database.database import get_all_achievements
from games_of_terminal.interface_manager import InterfaceManager
from games_of_terminal.log import log
from games_of_terminal.settings.achievements.achievement import Achievement
from games_of_terminal.settings.achievements.constants import (
    TITLE, BASE_OFFSET, TOP_OFFSET,
    LEFT_ARROW, RIGHT_ARROW, SIDE_ARROW_OFFSET,
    SIDE_OFFSET, BOTTOM_OFFSET, ACHIEVEMENTS_IN_ROW,
    ACHIEVEMENTS_SPACING, OFFSETS,
    ACH_NAME_COLOR_NAME, ACH_DESCRIPTION_COLOR_NAME,
    UPWARDS_ARROW, DOWNWARDS_ARROW, NO_ARROW,
)
from games_of_terminal.utils import (
    draw_message, clear_field_line, get_color_by_name,
)

from collections import defaultdict
from math import ceil


class Achievements(InterfaceManager):
    @log
    def __init__(self, canvas, settings_name):
        super().__init__(canvas, only_main_win=True)

        ach_height, ach_width = self.get_achievements_height_and_width()
        self.ach_height, self.ach_width = ach_height, ach_width

        self.settings_name = settings_name
        self.achievements = self.get_achievements()
        self.achievement_items = self.get_achievement_items()
        self.achievement_items_len = len(self.achievement_items)

        self.title_start_y = TOP_OFFSET
        self.game_name_y = self.get_game_name_y()
        self.achievements_start_y = self.get_achievements_start_y()

        self.showed_achievements_count = self.get_showed_achievements_count()

        self.left_arrow_x, self.right_arrow_x = self.get_arrows_xs()

        self.curr_game_ind = 0
        self.pagination_offset = 0
        self.max_pagination_offset = self.get_max_pagination_offset()

        # pagination arrows
        self.pag_arrow_x = self.width - (SIDE_OFFSET // 2)
        self.pag_up_arrow_y = self.achievements_start_y
        self.pag_down_arrow_y = self.height - BOTTOM_OFFSET - 1

        self.detail_mode = False
        self.selected_ach_num = 0

    def __repr__(self):
        return '<Achievements>'

    def get_achievement_items(self):
        return sorted(list(self.achievements.keys()))

    def get_achievement_by_number(self, number):
        for achievement in self.curr_achievements_list:
            if achievement.number == number:
                return achievement

    def get_achievements(self):
        all_achievements = get_all_achievements()
        achievements = defaultdict(list)

        for game_name, game_achievements in all_achievements.items():
            for achieve_num, achieve_data in enumerate(game_achievements):
                achievements[game_name].append(Achievement(
                    self.window, achieve_num,
                    self.ach_height, self.ach_width,
                    achieve_data
                ))

        return achievements

    def get_game_name_y(self):
        return self.title_start_y + len(TITLE) + BASE_OFFSET

    def get_achievements_start_y(self):
        return self.game_name_y + 1 + BASE_OFFSET

    def get_game_name_max_length(self):
        return max([len(game_name) for game_name in self.achievement_items])

    def get_arrows_xs(self):
        game_name_max_length = self.get_game_name_max_length()
        arrows_offset_length = SIDE_ARROW_OFFSET * 2
        arrows_length = len(LEFT_ARROW) + len(RIGHT_ARROW)
        game_name_line_len = (
                game_name_max_length + arrows_offset_length + arrows_length
        )

        left_arrow_x = (self.width // 2) - (game_name_line_len // 2)
        right_arrow_x = left_arrow_x + game_name_line_len - 1

        return left_arrow_x, right_arrow_x

    @property
    def curr_achievements_list(self):
        game_name = self.achievement_items[self.curr_game_ind]
        return self.achievements[game_name]

    @property
    def chosen_game_name(self):
        return self.achievement_items[self.curr_game_ind]

    @log
    def run(self):
        self.draw_title()
        self.show_achievements()

        while True:
            key = self.window.getch()
            self.wait_for_keypress()

            if key == KEYS['escape']:
                return
            elif key in KEYS['enter']:
                self.switch_detail_mode()
                self.switch_achieve_selection()
            elif key in (KEYS['up_arrow'], KEYS['w']):
                self.moving_controller('up')
            elif key in (KEYS['down_arrow'], KEYS['s']):
                self.moving_controller('down')
            elif key in (KEYS['left_arrow'], KEYS['a']):
                self.moving_controller('left')
            elif key in (KEYS['right_arrow'], KEYS['d']):
                self.moving_controller('right')

    def switch_detail_mode(self):
        self.detail_mode = not self.detail_mode

    def switch_achieve_selection(self):
        achieve = self.get_achievement_by_number(self.selected_ach_num)
        achieve.is_selected = not achieve.is_selected
        self.show_achieve(achieve)

    def moving_controller(self, direction):
        if self.detail_mode:
            self.select_cell(direction=direction)
            return

        if direction == 'left':
            self.update_current_game_index(-1)
        elif direction == 'right':
            self.update_current_game_index(1)

        self.reset_game_settings()
        self.show_pagination_arrows()
        self.clear_achievement_details()
        self.achievements_action(update_coords=True)

    @staticmethod
    def get_moving_offsets(key):
        for keys, offset in OFFSETS.items():
            if key in keys:
                return OFFSETS[keys]

    def reset_game_settings(self):
        self.selected_ach_num = 0
        self.pagination_offset = 0
        self.max_pagination_offset = self.get_max_pagination_offset()

    def select_cell(self, direction):
        y_offset, x_offset = self.get_moving_offsets(direction)
        chosen_ach_num = ((y_offset * ACHIEVEMENTS_IN_ROW) +
                          self.selected_ach_num +
                          x_offset)

        if not self.is_chosen_achieve_exists(chosen_ach_num):
            return

        # unselect current cell
        self.switch_achieve_selection()

        pagination_value = self.get_pagination_changing_value(
            direction, chosen_ach_num,
        )

        if pagination_value != 0:
            self.update_achievements_pagination(pagination_value)
            self.achievements_action(update_coords=True)

        # select chosen cell
        self.selected_ach_num = chosen_ach_num
        self.switch_achieve_selection()

    def update_current_game_index(self, direction):
        new_curr_game_index = self.curr_game_ind + direction

        if new_curr_game_index < 0:
            return
        if new_curr_game_index > self.achievement_items_len - 1:
            return

        self.curr_game_ind = new_curr_game_index
        self.show_achievements()

    def is_chosen_achieve_exists(self, chosen_ach_num):
        return 0 <= chosen_ach_num < len(self.curr_achievements_list)

    def get_pagination_changing_value(self, direction, ach_num):
        curr_ach_range = self.get_current_achievements_nums_range()

        if ach_num not in curr_ach_range:
            return 1 if direction in ['down', 'right'] else -1
        return 0

    def get_current_achievements_nums_range(self):
        ach_range_start = self.pagination_offset * ACHIEVEMENTS_IN_ROW
        ach_range_end = ach_range_start + self.showed_achievements_count

        return range(ach_range_start, ach_range_end)

    def show_achievement_details(self, achievement):
        self.clear_achievement_details()

        if not (self.detail_mode and achievement.is_selected):
            return

        achievement_details = self.get_prettify_achievement_details(
            achievement
        )
        start_y = self.height - (BOTTOM_OFFSET - 1)

        for y_offset, achievement_detail in enumerate(achievement_details):
            text = str(achievement_detail['text'])
            color_name = achievement_detail['color_name']
            color = get_color_by_name(color_name)

            y = start_y + y_offset
            x = (self.width // 2) - (len(text) // 2)

            draw_message(y, x, self.window, text, color)

    @staticmethod
    def get_prettify_achievement_details(achievement):
        prettify_status = str(achievement.status).capitalize()

        if achievement.date_received:
            prettify_status += ' ' + str(achievement.date_received)

        return [
            {'text': achievement.name,
             'color_name': ACH_NAME_COLOR_NAME},
            {'text': achievement.description,
             'color_name': ACH_DESCRIPTION_COLOR_NAME},
            {'text': prettify_status,
             'color_name': ''},
        ]

    def clear_achievement_details(self):
        for y in range(self.height - BOTTOM_OFFSET, self.height):
            clear_field_line(y, SIDE_OFFSET, self.window,
                             self.width - (SIDE_OFFSET * 2))

    def show_achievements(self):
        self.show_game_name_with_arrows()
        self.show_pagination_arrows()
        self.achievements_action(update_coords=True)

    @log(with_runtime=True)
    def achievements_action(self, show=True, update_coords=False):
        self.clear_achievements_body()

        y = self.achievements_start_y
        x = start_x = SIDE_OFFSET

        ach_num = ACHIEVEMENTS_IN_ROW
        ach_offset_start = self.pagination_offset * ACHIEVEMENTS_IN_ROW

        for achieve in self.curr_achievements_list[ach_offset_start:]:
            if y + self.ach_height > self.height - BOTTOM_OFFSET:
                return

            if update_coords:
                achieve.update_coordinates(y, x)
            if show:
                self.show_achieve(achieve)

            if ach_num == 1:
                ach_num = ACHIEVEMENTS_IN_ROW
                y += self.ach_height + BASE_OFFSET
                x = start_x
            else:
                ach_num -= 1
                x += self.ach_width + ACHIEVEMENTS_SPACING

    def clear_achievements_body(self):
        curr_y = self.achievements_start_y
        curr_x = SIDE_OFFSET

        curr_height = self.height - self.achievements_start_y
        clear_line_width = self.width - (SIDE_OFFSET * 2)

        for y_offset in range(curr_height):
            clear_field_line(curr_y + y_offset, curr_x, self.window,
                             clear_line_width)

    def show_achieve(self, achieve):
        achieve.show()
        self.show_achievement_details(achieve)

    def get_showed_achievements_count(self):
        showed_achievements_count = 0
        y = self.achievements_start_y

        while y + self.ach_height <= self.height - BOTTOM_OFFSET:
            showed_achievements_count += ACHIEVEMENTS_IN_ROW
            y += self.ach_height + BASE_OFFSET

        return showed_achievements_count

    def get_max_pagination_offset(self):
        visible_rows = 0
        rows_with_achievs = ceil(
            len(self.curr_achievements_list) / ACHIEVEMENTS_IN_ROW
        )
        achievs_place_height = (
            self.height - self.achievements_start_y - BOTTOM_OFFSET
        )

        while True:
            achievs_place_height -= self.ach_height

            if achievs_place_height < 0:
                break

            achievs_place_height -= BASE_OFFSET
            visible_rows += 1

        return max(rows_with_achievs - visible_rows, 0)

    def get_achievements_height_and_width(self):
        width = ((self.width -
                  (SIDE_OFFSET * 2) -
                  ((ACHIEVEMENTS_IN_ROW - 1) * ACHIEVEMENTS_SPACING))
                 // ACHIEVEMENTS_IN_ROW)

        width -= 1 if (width % 2 != 0) else 0
        height = width // 2

        return height, width

    def show_game_name_with_arrows(self):
        self.clear_game_name_line()
        self.draw_game_name_left_arrow()
        self.draw_game_name()
        self.draw_game_name_right_arrow()

    def draw_game_name(self):
        game_name_len = len(self.chosen_game_name)
        game_name_x = (self.width // 2) - (game_name_len // 2)

        draw_message(
            self.game_name_y, game_name_x,
            self.window, self.chosen_game_name,
        )

    def draw_game_name_left_arrow(self):
        if self.curr_game_ind == 0:
            return

        draw_message(
            self.game_name_y, self.left_arrow_x,
            self.window, LEFT_ARROW,
        )

    def draw_game_name_right_arrow(self):
        if self.curr_game_ind == self.achievement_items_len - 1:
            return

        draw_message(
            self.game_name_y, self.right_arrow_x,
            self.window, RIGHT_ARROW,
        )

    def clear_game_name_line(self):
        clear_field_line(
            self.game_name_y, 1,
            self.window, self.width - BASE_OFFSET,
        )

    def update_achievements_pagination(self, direction):
        new_pagination_offset = self.pagination_offset + direction

        if new_pagination_offset < 0:
            return
        if new_pagination_offset > self.max_pagination_offset:
            return

        self.pagination_offset = new_pagination_offset
        self.show_pagination_arrows()

    def show_pagination_arrows(self):
        up_arrow = UPWARDS_ARROW
        down_arrow = DOWNWARDS_ARROW

        if self.max_pagination_offset == 0:
            up_arrow = down_arrow = NO_ARROW
        if self.pagination_offset == 0:
            up_arrow = NO_ARROW
        if self.pagination_offset == self.max_pagination_offset:
            down_arrow = NO_ARROW

        draw_message(self.pag_up_arrow_y, self.pag_arrow_x,
                     self.window, up_arrow)
        draw_message(self.pag_down_arrow_y, self.pag_arrow_x,
                     self.window, down_arrow)

    def draw_title(self):
        for y, line in enumerate(TITLE, start=self.title_start_y):
            x = (self.width // 2) - (len(line) // 2)
            draw_message(y, x, self.window, line)
