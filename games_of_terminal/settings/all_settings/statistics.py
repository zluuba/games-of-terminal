from games_of_terminal.app_interface import InterfaceManager
from games_of_terminal.database.database import get_games_statistic
from games_of_terminal.utils import draw_message, get_color_by_name, clear_field_line
from games_of_terminal.constants import KEYS, DEFAULT_COLOR, GAMES


LOGO = [
    '▄ █▀ ▀█▀ ▄▀█ ▀█▀ █ █▀ ▀█▀ █ █▀▀ ▄',
    '  ▄█  █  █▀█  █  █ ▄█  █  █ █▄▄  ',
]

UPWARDS_ARROW = '▲'
DOWNWARDS_ARROW = '▼'
BOTTOM_OFFSET = 2


class Statistics(InterfaceManager):
    def __init__(self, canvas, settings_name):
        super().__init__(canvas, only_main_win=True)

        self.settings_name = settings_name
        statistic_raw_data = get_games_statistic()
        self.statistics_data = self.get_statistics_list_data(statistic_raw_data)

        self.logo_start_y = 3
        self.start_y = self.logo_start_y + len(LOGO) + 2

        self.pagination_offset = 0
        self.max_pagination_offset = len(self.statistics_data) - (self.height - self.start_y) + len(GAMES) - 1

        self.max_elem_width = max([len(elem[1]) for elem in self.statistics_data])
        self.arrow_x = (self.width // 2) + max((self.max_elem_width // 2) + 4, len(LOGO[0]) // 2)

        # self.normalize_statistics_data()

    def run(self):
        self.draw_logo()
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

    def draw_logo(self):
        for y, line in enumerate(LOGO, start=self.logo_start_y):
            x = (self.width // 2) - (len(line) // 2)
            draw_message(y, x, self.window, line, DEFAULT_COLOR)

    def draw_arrows(self):
        up_arrow = UPWARDS_ARROW if self.pagination_offset else ' '
        draw_message(self.start_y, self.arrow_x, self.window, up_arrow, DEFAULT_COLOR)

        down_arrow = DOWNWARDS_ARROW if self.pagination_offset < self.max_pagination_offset else ' '
        draw_message(self.height - BOTTOM_OFFSET, self.arrow_x, self.window, down_arrow, DEFAULT_COLOR)

    def show_statistics(self):
        game_name_color = get_color_by_name('strong_pastel_purple_text_black_bg')
        stat_y = self.start_y

        for type_, data in self.statistics_data[self.pagination_offset:]:
            if stat_y != self.start_y and type_ == 'game_name':
                self.draw_stat_elem(stat_y, '')
                stat_y += 1

            color = DEFAULT_COLOR if type_ == 'stat' else game_name_color
            self.draw_stat_elem(stat_y, data, color)

            stat_y += 1

    def draw_stat_elem(self, y, message, color=DEFAULT_COLOR):
        if y > self.height - BOTTOM_OFFSET:
            return

        clear_line_x = (self.width // 2) - (self.max_elem_width // 2)
        clear_field_line(y, clear_line_x, self.window, self.max_elem_width)

        draw_elem_x = (self.width // 2) - (len(message) // 2)
        draw_message(y, draw_elem_x, self.window, message, color)

    @staticmethod
    def get_statistics_list_data(statistics_dict):
        statistics_list_data = []

        for game_name, game_data in statistics_dict.items():
            statistics_list_data.append(('game_name', game_name))

            for stat_name, stat_data in game_data.items():
                stat = f'{stat_name}: {stat_data}'
                statistics_list_data.append(('stat', stat))

        return statistics_list_data

    def normalize_statistics_data(self):
        normalized_statistics_data = []

        for type_, data in self.statistics_data:
            if type_ == 'game_name':
                normalized_statistics_data.append((type_, data))
                continue

            stat_name, stat_data = data
            stat_name = ' '.join(map(lambda word: word.capitalize(), stat_name.split('_')))
            spaces = self.max_elem_width - (len(stat_name) + len(str(stat_data)))
            stat = f'{stat_name}: {" " * spaces}{stat_data}'
            normalized_statistics_data.append((type_, stat))

        self.statistics_data = normalized_statistics_data
