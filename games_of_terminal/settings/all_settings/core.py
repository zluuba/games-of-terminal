from games_of_terminal.constants import (
    KEYS, BASE_OFFSET,
)
from games_of_terminal.database.database import get_all_settings
from games_of_terminal.interface_manager import InterfaceManager
from games_of_terminal.utils import (
    draw_message, clear_field_line,
)
from games_of_terminal.settings.all_settings.constants import (
    TITLE, TOP_OFFSET, SIDE_ARROW_OFFSET,
    LEFT_ARROW, RIGHT_ARROW, NO_ARROW,
    UPWARDS_ARROW, DOWNWARDS_ARROW,
    BOTTOM_OFFSET,
)


class GamesSettings(InterfaceManager):
    def __init__(self, canvas, name):
        super().__init__(canvas, only_main_win=True)

        self.name = name

        self.all_settings = get_all_settings()
        self.items = list(self.all_settings.keys())
        self.items_len = len(self.items)

        self.title_start_y = TOP_OFFSET

        self.setup_vars()

    def setup_vars(self):
        self.curr_game_ind = 0
        self.detail_mode = False

        self.curr_option_ind = 0

        self.pagination_offset = 0

        self.game_name_y = self.get_game_name_y()
        self.settings_start_y = self.get_settings_start_y()

        self.left_arrow_x, self.right_arrow_x = self.get_arrows_xs()

        self.max_pagination_offset = self.get_max_pagination_offset()

    def get_max_pagination_offset(self):
        return ((self.items_len + self.items_len) -
                (self.height - self.settings_start_y) - BOTTOM_OFFSET - 1)

    def get_game_name_y(self):
        return self.title_start_y + len(TITLE) + BASE_OFFSET

    def get_settings_start_y(self):
        return self.game_name_y + BASE_OFFSET + 1

    def get_setting_name_max_length(self):
        return max([len(game_name) for game_name in self.items])

    @property
    def chosen_game_name(self):
        return self.items[self.curr_game_ind]

    @property
    def options(self):
        return self.all_settings[self.chosen_game_name]

    @property
    def current_option(self):
        return

    @property
    def current_option_values(self):
        return

    def get_arrows_xs(self):
        game_name_max_length = self.get_setting_name_max_length()
        arrows_offset_length = SIDE_ARROW_OFFSET * 2
        arrows_length = len(LEFT_ARROW) + len(RIGHT_ARROW)
        game_name_line_len = (
                game_name_max_length + arrows_offset_length + arrows_length
        )

        left_arrow_x = (self.width // 2) - (game_name_line_len // 2)
        right_arrow_x = left_arrow_x + game_name_line_len - 1

        return left_arrow_x, right_arrow_x

    def run(self):
        self.draw_title()
        self.show_settings()

        while True:
            key = self.window.getch()
            self.wait_for_keypress()

            if key == KEYS['escape']:
                return
            elif key == KEYS['resize']:
                self.window.timeout(0)
                self.resize_menu_win_handler(key)
            elif key in KEYS['enter']:
                self.switch_detail_mode()
                self.switch_all_settings_selection()
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

    def switch_selection_mode(self):
        pass

    def moving_controller(self, direction):
        # if self.detail_mode:
        #     self.select_option(direction=direction)
        #     return

        if direction == 'left':
            self.update_current_game_index(-1)
        elif direction == 'right':
            self.update_current_game_index(1)
        else:
            return

        # self.reset_game_settings()
        # self.show_pagination_arrows()
        # self.clear_achievement_details()
        # self.achievements_action(show=True, update_coords=True)

    def update_current_game_index(self, direction):
        new_curr_game_index = self.curr_game_ind + direction

        if new_curr_game_index < 0:
            return
        if new_curr_game_index > self.items_len - 1:
            return

        self.clear_options_area()
        self.curr_game_ind = new_curr_game_index
        self.show_settings()

    def show_settings(self):
        self.show_game_name_with_arrows()
        self.show_options()
        # self.show_pagination_arrows()
        # self.settings_action(show=True, update_coords=True)

    def show_options(self):
        for y_offset, option in enumerate(self.options):
            y = self.settings_start_y + y_offset
            x = (self.width // 2) - (len(option) // 2)
            draw_message(y, x, self.window, self.prettify_option(option))

    def clear_options_area(self):
        for y_offset, option in enumerate(self.options):
            y = self.settings_start_y + y_offset
            x = (self.width // 2) - (len(option) // 2)
            empty_line_width = len(option)

            clear_field_line(y, x, self.window, empty_line_width)

    @staticmethod
    def prettify_option(option):
        return ' '.join(map(lambda word: word.capitalize(), option.split('_')))

    def show_pagination_arrows(self):
        up_arrow = UPWARDS_ARROW
        down_arrow = DOWNWARDS_ARROW

        if not self.pagination_offset:
            up_arrow = NO_ARROW
        if self.pagination_offset >= self.max_pagination_offset:
            down_arrow = NO_ARROW

        draw_message(self.start_y, self.arrow_x, self.window, up_arrow)

        down_arrow_y = self.height - BOTTOM_OFFSET
        draw_message(down_arrow_y, self.arrow_x, self.window, down_arrow)

    def show_game_name_with_arrows(self):
        self.clear_game_name_line()
        self.draw_game_name_left_arrow()
        self.draw_game_name()
        self.draw_game_name_right_arrow()

    def clear_game_name_line(self):
        clear_field_line(
            self.game_name_y, 1,
            self.window, self.width - BASE_OFFSET,
        )

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
        if self.curr_game_ind == self.items_len - 1:
            return

        draw_message(
            self.game_name_y, self.right_arrow_x,
            self.window, RIGHT_ARROW,
        )

    def draw_title(self):
        for y, line in enumerate(TITLE, start=self.title_start_y):
            x = (self.width // 2) - (len(line) // 2)
            draw_message(y, x, self.window, line)

    def redraw_window(self):
        self.setup_vars()
        self.show_settings()
