from games_of_terminal.constants import KEYS, DEFAULT_COLOR, GAMES
from games_of_terminal.database.database import get_all_achievements
from games_of_terminal.interface_manager import InterfaceManager
from games_of_terminal.log import log
from games_of_terminal.settings.achievements.constants import (
    TITLE, BASE_OFFSET, TOP_OFFSET,
    LEFT_ARROW, RIGHT_ARROW, SIDE_ARROW_OFFSET,
    SIDE_OFFSET, BOTTOM_OFFSET, ACHIEVEMENTS_IN_ROW,
    ACHIEVEMENTS_SPACING,
)
from games_of_terminal.utils import (
    draw_message, clear_field_line,
)

from math import ceil


class Achievements(InterfaceManager):
    @log
    def __init__(self, canvas, settings_name):
        super().__init__(canvas, only_main_win=True)

        self.settings_name = settings_name
        # {game_name: [{name, status, description}, {...}]}
        self.achievements = get_all_achievements()

        self.ach_height, self.ach_width = self.get_achievements_height_and_width()

        self.title_start_y = TOP_OFFSET
        self.game_name_y = self.get_game_name_y()
        self.achievements_start_y = self.get_achievements_start_y()

        self.left_arrow_x, self.right_arrow_x = self.get_arrows_xs()

        self.curr_game_ind = 0
        self.pagination_offset = 0
        self.max_pagination_offset = self.get_max_pagination_offset()

    def __repr__(self):
        return f'<Achievements>'

    @property
    def curr_achievements_list(self):
        game_name = GAMES[self.curr_game_ind]
        return self.achievements[game_name]

    def get_game_name_y(self):
        return self.title_start_y + len(TITLE) + BASE_OFFSET

    def get_achievements_start_y(self):
        return self.game_name_y + BASE_OFFSET

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
    def chosen_game_game(self):
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
            elif key in (KEYS['up_arrow'], KEYS['w']):
                self.update_achievements_pagination(-1)
            elif key in (KEYS['down_arrow'], KEYS['s']):
                self.update_achievements_pagination(1)
            elif key in (KEYS['left_arrow'], KEYS['a']):
                self.update_current_game_index(-1)
            elif key in (KEYS['right_arrow'], KEYS['d']):
                self.update_current_game_index(1)

    def show_achievements(self):
        self.show_game_name_with_arrows()
        self.show_achievements_body()
        self.get_max_pagination_offset()

    def show_achievements_body(self):
        height, width = self.get_achievements_height_and_width()

        y = self.achievements_start_y
        x = start_x = SIDE_OFFSET

        msg = '.' * width

        while True:
            if y + height > self.height - BOTTOM_OFFSET:
                return

            for _ in range(height):
                for _ in range(ACHIEVEMENTS_IN_ROW):
                    draw_message(y, x, self.window, msg, DEFAULT_COLOR)
                    x += width + ACHIEVEMENTS_SPACING

                x = start_x
                y += 1

            x = start_x
            y += BASE_OFFSET

    def get_max_pagination_offset(self):
        rows_with_achievs = ceil(len(self.curr_achievements_list) / ACHIEVEMENTS_IN_ROW)
        visible_rows = 0

        achievs_place_height = self.height - self.achievements_start_y - BOTTOM_OFFSET

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
        height = width // 2

        return height, width

    def show_game_name_with_arrows(self):
        left_arrow = LEFT_ARROW
        right_arrow = RIGHT_ARROW

        if self.curr_game_ind == 0:
            left_arrow = ' '
        if self.curr_game_ind == len(GAMES) - 1:
            right_arrow = ' '

        game_name_x = (self.width // 2) - (len(self.chosen_game_game) // 2)

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
            self.window, self.chosen_game_game, DEFAULT_COLOR,
        )
        draw_message(
            self.game_name_y, self.right_arrow_x,
            self.window, right_arrow, DEFAULT_COLOR,
        )

    @log
    def update_achievements_pagination(self, direction):
        new_pagination_offset = self.pagination_offset + direction

        if new_pagination_offset < 0:
            return
        if new_pagination_offset > self.max_pagination_offset:
            return

        self.pagination_offset = new_pagination_offset
        self.show_achievements()

    @log
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
