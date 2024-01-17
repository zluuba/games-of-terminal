from games_of_terminal.constants import KEYS, DEFAULT_COLOR, GAMES
from games_of_terminal.database.database import get_all_achievements
from games_of_terminal.interface_manager import InterfaceManager
from games_of_terminal.log import log
from games_of_terminal.settings.achievements.achievement import Achievement
from games_of_terminal.settings.achievements.constants import (
    TITLE, BASE_OFFSET, TOP_OFFSET,
    LEFT_ARROW, RIGHT_ARROW, SIDE_ARROW_OFFSET,
    SIDE_OFFSET, BOTTOM_OFFSET, ACHIEVEMENTS_IN_ROW,
    ACHIEVEMENTS_SPACING,
)
from games_of_terminal.utils import (
    draw_message, clear_field_line,
    get_color_by_name,
)

from collections import defaultdict
from math import ceil


class Achievements(InterfaceManager):
    @log
    def __init__(self, canvas, settings_name):
        super().__init__(canvas, only_main_win=True)

        self.showed_achievements_count = 0

        self.settings_name = settings_name
        self.ach_height, self.ach_width = self.get_achievements_height_and_width()
        self.achievements = self.get_achievements()

        self.title_start_y = TOP_OFFSET
        self.game_name_y = self.get_game_name_y()
        self.achievements_start_y = self.get_achievements_start_y()

        self.left_arrow_x, self.right_arrow_x = self.get_arrows_xs()

        self.curr_game_ind = 0
        self.pagination_offset = 0
        self.max_pagination_offset = self.get_max_pagination_offset()

        self.detail_mode = False
        self.selected_ach_num = 0

    def __repr__(self):
        return f'<Achievements>'

    def get_achievement_by_number(self, number):
        for achievement in self.curr_achievements_list:
            if achievement.number == number:
                return achievement

    def switch_achieve_selection(self):
        for ach_num, achieve in enumerate(self.curr_achievements_list, start=0):
            if ach_num == self.selected_ach_num:
                achieve.is_selected = not achieve.is_selected

    def get_achievements(self):
        # {game_name: [{name, status, description}, {...}]}
        all_achievements = get_all_achievements()
        achievements = defaultdict(list)

        for game_name, achievements_ in all_achievements.items():
            for achieve_num, achieve_data in enumerate(achievements_, start=0):
                new_achieve = Achievement(self.window, achieve_num, self.ach_height, self.ach_width, achieve_data)
                achievements[game_name].append(new_achieve)

        return achievements

    @property
    def curr_achievements_list(self):
        game_name = GAMES[self.curr_game_ind]
        return self.achievements[game_name]

    def get_game_name_y(self):
        return self.title_start_y + len(TITLE) + BASE_OFFSET

    def get_achievements_start_y(self):
        return self.game_name_y + 1 + BASE_OFFSET

    @staticmethod
    def get_game_name_max_length():
        return max([len(game_name) for game_name in GAMES])

    def get_arrows_xs(self):
        game_name_max_length = self.get_game_name_max_length()
        arrows_offset_length = SIDE_ARROW_OFFSET * 2
        arrows_length = len(LEFT_ARROW) + len(RIGHT_ARROW)
        game_name_line_len = (
                game_name_max_length + arrows_offset_length + arrows_length
        )

        left_arrow_x = (self.width // 2) - (game_name_line_len // 2)
        right_arrow_x = left_arrow_x + game_name_line_len

        # horizontal alignment
        right_arrow_x -= 1

        return left_arrow_x, right_arrow_x

    @property
    def chosen_game_name(self):
        return GAMES[self.curr_game_ind]

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
                self.update_achievements_pagination(-1)
            elif key in (KEYS['down_arrow'], KEYS['s']):
                self.update_achievements_pagination(1)
            elif key in (KEYS['left_arrow'], KEYS['a']):
                if self.detail_mode:
                    self.select_cell(x_offset=-1)
                else:
                    self.update_current_game_index(-1)
            elif key in (KEYS['right_arrow'], KEYS['d']):
                if self.detail_mode:
                    self.select_cell(x_offset=1)
                else:
                    self.update_current_game_index(1)

    def select_cell(self, y_offset=0, x_offset=0):
        all_curr_achievements_count = len(self.curr_achievements_list)

        chosen_num_x = self.selected_ach_num + x_offset

        if (chosen_num_x // ACHIEVEMENTS_IN_ROW) != (self.selected_ach_num // ACHIEVEMENTS_IN_ROW):
            return

        chosen_num_xy = chosen_num_x + (y_offset * 5)

        if 0 <= chosen_num_xy < all_curr_achievements_count:
            curr_selected = self.get_achievement_by_number(self.selected_ach_num)
            curr_selected.is_selected = not curr_selected.is_selected

            self.selected_ach_num = chosen_num_xy
            new_selected = self.get_achievement_by_number(self.selected_ach_num)
            new_selected.is_selected = not new_selected.is_selected

            self.show_achievements_body()

    def switch_detail_mode(self):
        self.selected_ach = 0
        self.detail_mode = not self.detail_mode

    def show_achievements(self):
        self.show_game_name_with_arrows()
        self.show_achievements_body()

    def clear_achievements_body(self):
        curr_y = self.achievements_start_y
        curr_x = SIDE_OFFSET

        curr_height = self.height - self.achievements_start_y - BASE_OFFSET
        clear_line_width = self.width - (SIDE_OFFSET * 2)

        for y_offset in range(curr_height):
            clear_field_line(curr_y + y_offset, curr_x, self.window, clear_line_width)

    @log(with_runtime=True)
    def show_achievements_body(self):
        # runtime min: 20.47ms, max: 36.09ms
        self.clear_achievements_body()

        y = self.achievements_start_y
        x = start_x = SIDE_OFFSET
        ach_num = 4

        for achieve in self.curr_achievements_list:
            if y + self.ach_height > self.height - BOTTOM_OFFSET:
                return

            curr_y = y
            curr_x = x
            color_ind = 0

            for ach_y, _ in enumerate(range(self.ach_height), start=curr_y):
                for ach_x, _ in enumerate(range(self.ach_width), start=curr_x):
                    self.draw_achieve_cell(ach_y, ach_x, achieve, color_ind)
                    self.showed_achievements_count += 1
                    color_ind += 1
                curr_x = x

            if not ach_num:
                ach_num = 4
                y += self.ach_height + BASE_OFFSET
                x = start_x
            else:
                ach_num -= 1
                x = curr_x + self.ach_width + ACHIEVEMENTS_SPACING

    def draw_achieve_cell(self, y, x, achieve, color_ind):
        achieve_cell = ' '
        color_name = achieve.get_picture_color_by_index(color_ind)
        color = get_color_by_name(color_name)
        draw_message(y, x, self.window, achieve_cell, color)

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

        return max(visible_rows - rows_with_achievs, 0)

    def get_achievements_height_and_width(self):
        width = ((self.width -
                  (SIDE_OFFSET * 2) -
                  ((ACHIEVEMENTS_IN_ROW - 1) * ACHIEVEMENTS_SPACING))
                 // ACHIEVEMENTS_IN_ROW)

        width -= 1 if (width % 2 != 0) else 0
        height = width // 2

        return height, width

    def show_game_name_with_arrows(self):
        left_arrow = LEFT_ARROW
        right_arrow = RIGHT_ARROW

        if self.curr_game_ind == 0:
            left_arrow = ' '
        if self.curr_game_ind == len(GAMES) - 1:
            right_arrow = ' '

        game_name_x = (self.width // 2) - (len(self.chosen_game_name) // 2)

        clear_field_line(
            self.game_name_y, 1,
            self.window, self.width - 2,
        )
        draw_message(
            self.game_name_y, self.left_arrow_x,
            self.window, left_arrow, DEFAULT_COLOR,
        )
        draw_message(
            self.game_name_y, game_name_x,
            self.window, self.chosen_game_name, DEFAULT_COLOR,
        )
        draw_message(
            self.game_name_y, self.right_arrow_x,
            self.window, right_arrow, DEFAULT_COLOR,
        )

    def update_achievements_pagination(self, direction):
        new_pagination_offset = self.pagination_offset + direction

        if new_pagination_offset < 0:
            return
        if new_pagination_offset > self.max_pagination_offset:
            return

        self.pagination_offset = new_pagination_offset
        self.show_achievements()

    def update_current_game_index(self, direction):
        new_curr_game_index = self.curr_game_ind + direction

        if new_curr_game_index < 0:
            return
        if new_curr_game_index > len(GAMES) - 1:
            return

        self.curr_game_ind = new_curr_game_index
        self.show_achievements()

    def draw_title(self):
        for y, line in enumerate(TITLE, start=self.title_start_y):
            x = (self.width // 2) - (len(line) // 2)
            draw_message(y, x, self.window, line, DEFAULT_COLOR)
