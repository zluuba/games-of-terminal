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
    0: {'name': 'All Settings', 'class': GamesSettings, 'status': 'production'},
    1: {'name': 'Achievements', 'class': Achievements, 'status': 'production'},
    2: {'name': 'Statistics', 'class': Statistics, 'status': 'production'},
    3: {'name': 'Reset All', 'class': ResetAll, 'status': 'production'},
    4: {'name': 'Confess All', 'class': ConfessAll, 'status': 'in_development'},
}

ITEMS_LEN = len(ITEMS)

CONFESS_TEXT = """
Congratulations! You've almost confessed everything. 
Don't worry, we won't judge. 
On a serious note, you can send your game statistics to me, the developer, which 
makes me happy because I want to know that some pure soul is playing the games I've 
created so diligently.
And I'll give you something special for your secrets!
"""
# + buttons "Send Data" and "Do Not Send Data"
