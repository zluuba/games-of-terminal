from games_of_terminal.constants import KEYS, DEFAULT_COLOR, GAMES
from games_of_terminal.database.database import get_games_statistic
from games_of_terminal.interface_manager import InterfaceManager
from games_of_terminal.settings.statistics.constants import (
    TITLE, UPWARDS_ARROW, DOWNWARDS_ARROW, TOP_OFFSET,
    BOTTOM_OFFSET, BASE_OFFSET, ARROWS_OFFSET,
)
from games_of_terminal.utils import (
    draw_message, get_color_by_name, clear_field_line,
)


class Statistics(InterfaceManager):
    def __init__(self, canvas, settings_name):
        super().__init__(canvas, only_main_win=True)

        self.settings_name = settings_name

        statistic_raw_data = get_games_statistic()
        self.max_elem_width = self.get_max_elem_width(
            statistic_raw_data
        )
        self.statistics_data = self.get_statistics_prettify_data(
            statistic_raw_data
        )

        self.logo_start_y = TOP_OFFSET
        self.start_y = self.get_statistic_elements_start_y()

        self.pagination_offset = 0
        self.max_pagination_offset = self.get_max_pagination_offset()

        self.arrow_x = self.get_arrow_x()

    def get_max_pagination_offset(self):
        return (len(self.statistics_data) + len(GAMES) -
                (self.height - self.start_y) - 1)

    def get_arrow_x(self):
        return (self.width // 2) + max(
            (self.max_elem_width // 2) + ARROWS_OFFSET,
            len(TITLE[0]) // 2,
        )

    def get_statistic_elements_start_y(self):
        return self.logo_start_y + len(TITLE) + BASE_OFFSET

    def run(self):
        self.draw_title()
        self.draw_arrows()
        self.show_statistics()

        while True:
            key = self.window.getch()
            self.wait_for_keypress()

            if key == KEYS['escape']:
                return
            elif key in (KEYS['up_arrow'], KEYS['w']):
                self.update_statistics_pagination(-1)
            elif key in (KEYS['down_arrow'], KEYS['s']):
                self.update_statistics_pagination(1)

    def update_statistics_pagination(self, direction):
        new_pagination_offset = self.pagination_offset + direction

        if new_pagination_offset < 0:
            return
        if new_pagination_offset > self.max_pagination_offset:
            return

        self.pagination_offset = new_pagination_offset
        self.show_statistics()
        self.draw_arrows()

    def draw_title(self):
        for y, line in enumerate(TITLE, start=self.logo_start_y):
            x = (self.width // 2) - (len(line) // 2)
            draw_message(y, x, self.window, line, DEFAULT_COLOR)

    def draw_arrows(self):
        up_arrow = UPWARDS_ARROW
        down_arrow = DOWNWARDS_ARROW

        if not self.pagination_offset:
            up_arrow = ' '
        if self.pagination_offset >= self.max_pagination_offset:
            down_arrow = ' '

        draw_message(
            self.start_y, self.arrow_x,
            self.window, up_arrow, DEFAULT_COLOR,
        )

        draw_message(
            self.height - BOTTOM_OFFSET, self.arrow_x,
            self.window, down_arrow, DEFAULT_COLOR
        )

    def show_statistics(self):
        game_name_color = get_color_by_name('yellow_text_black_bg')
        stat_y = self.start_y

        for type_, data in self.statistics_data[self.pagination_offset:]:
            if stat_y != self.start_y and type_ == 'game_name':
                # draw an empty line to visually separate the games
                self.draw_stat_elem(stat_y, '')
                stat_y += 1

            color = DEFAULT_COLOR if type_ == 'stat' else game_name_color
            self.draw_stat_elem(stat_y, data, color)

            stat_y += 1

    def draw_stat_elem(self, y, message, color=DEFAULT_COLOR):
        if y > self.height - BOTTOM_OFFSET:
            return

        clear_line_x = (self.width // 2) - (self.max_elem_width // 2) - 1
        clear_field_line(y, clear_line_x, self.window,
                         self.max_elem_width + BASE_OFFSET)

        draw_elem_x = (self.width // 2) - (len(message) // 2)
        draw_message(y, draw_elem_x, self.window, message, color)

    def get_statistics_prettify_data(self, statistics_dict):
        statistics_prettify_data = []

        for game_name, game_data in statistics_dict.items():
            statistics_prettify_data.append(('game_name', game_name))

            for stat_name, stat_data in game_data.items():
                stat_name, stat_data = str(stat_name), str(stat_data)
                stat_name = self.get_normalized_stat_name(stat_name)
                spaces = self.get_spaces_count(stat_name, stat_data)
                prettify_stat = stat_name + ':' + (' ' * spaces) + stat_data
                statistics_prettify_data.append(('stat', prettify_stat))

        return statistics_prettify_data

    def get_spaces_count(self, *args):
        chars_count = sum(map(lambda word: len(word), args))
        return self.max_elem_width - chars_count

    @staticmethod
    def get_normalized_stat_name(stat_name):
        return ' '.join(
            map(lambda word: word.capitalize(), stat_name.split('_'))
        )

    @staticmethod
    def get_max_elem_width(statistics_dict):
        elements_width = [
            len(f'{stat_name}{stat_data}') + BASE_OFFSET
            for game_data in statistics_dict.values()
            for stat_name, stat_data in game_data.items()
        ]

        return max(elements_width)
