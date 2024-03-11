from games_of_terminal.settings.all_settings.core import GamesSettings
from games_of_terminal.settings.achievements.core import Achievements
from games_of_terminal.settings.statistics.core import Statistics
from games_of_terminal.settings.reset_all.core import ResetAll
from games_of_terminal.settings.confess_all.core import ConfessAll


TITLE = [
    '   ░█▀▀▀█ ░█▀▀▀ ▀▀█▀▀ ▀▀█▀▀ ▀█▀ ░█▄ ░█ ░█▀▀█ ░█▀▀▀█   ',
    ' ▀  ▀▀▀▄▄ ░█▀▀▀  ░█    ░█   ░█  ░█░█░█ ░█ ▄▄  ▀▀▀▄▄ ▀ ',
    '   ░█▄▄▄█ ░█▄▄▄  ░█    ░█   ▄█▄ ░█  ▀█ ░█▄▄█ ░█▄▄▄█   ',
]

ITEMS = {
    0: {'name': 'All Settings',
        'class': GamesSettings,
        'status': 'production'},

    1: {'name': 'Achievements',
        'class': Achievements,
        'status': 'production'},

    2: {'name': 'Statistics',
        'class': Statistics,
        'status': 'production'},

    3: {'name': 'Reset All',
        'class': ResetAll,
        'status': 'production'},

    4: {'name': 'Confess All',
        'class': ConfessAll,
        'status': 'in_development'},
}

NOISE_CHARS = ['.', '-', '-', '_', '_', '|', '|']
NOISE_CHARS_LEN = len(NOISE_CHARS)
NOISE_COLOR_NAME = 'grey_text_black_bg'

# the lower the number, the more noise there will be
NOISE_ANIMATION_DIV = 3

TITLE_OFFSET = 3
