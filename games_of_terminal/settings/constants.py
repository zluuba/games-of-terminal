from .all_settings.user_preferences import UserPreferences
from .all_settings.games_settings import GamesSettings
from .all_settings.achievements import Achievements
from .all_settings.statistics import Statistics
from .all_settings.reset_all import ResetAll
from .all_settings.confess_all import ConfessAll


TITLE = [
    '   ░█▀▀▀█ ░█▀▀▀ ▀▀█▀▀ ▀▀█▀▀ ▀█▀ ░█▄ ░█ ░█▀▀█ ░█▀▀▀█   ',
    ' ▀  ▀▀▀▄▄ ░█▀▀▀  ░█    ░█   ░█  ░█░█░█ ░█ ▄▄  ▀▀▀▄▄ ▀ ',
    '   ░█▄▄▄█ ░█▄▄▄  ░█    ░█   ▄█▄ ░█  ▀█ ░█▄▄█ ░█▄▄▄█   ',
]

ITEMS = {
    0: {'name': 'User Preferences', 'class': UserPreferences, 'status': 'in_development'},
    1: {'name': 'Games Settings', 'class': GamesSettings, 'status': 'production'},
    2: {'name': 'Achievements', 'class': Achievements, 'status': 'production'},
    3: {'name': 'Statistics', 'class': Statistics, 'status': 'production'},
    4: {'name': 'Reset All', 'class': ResetAll, 'status': 'in_development'},
    5: {'name': 'Confess All', 'class': ConfessAll, 'status': 'in_development'},
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
