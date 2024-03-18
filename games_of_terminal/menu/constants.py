from games_of_terminal.games.snake.core import SnakeGame
from games_of_terminal.games.minesweeper.core import MinesweeperGame
from games_of_terminal.games.tictactoe.core import TicTacToeGame
from games_of_terminal.games.tetris.core import TetrisGame
from games_of_terminal.settings.core import Settings


MENU_ITEMS = [
    {'name': 'Tetris', 'class': TetrisGame, 'type': 'game'},
    {'name': 'Minesweeper', 'class': MinesweeperGame, 'type': 'game'},
    {'name': 'Tic Tac Toe', 'class': TicTacToeGame, 'type': 'game'},
    {'name': 'Snake', 'class': SnakeGame, 'type': 'game'},

    # ------ Settings should come last ------
    {'name': 'Settings', 'class': Settings, 'type': 'settings'},
]

MENU_ITEMS_COUNT = len(MENU_ITEMS)

GOODBYE_MESSAGES = [
    'Already miss you.', 'You\'re a geek, right?',
    'Have a great day, babe', 'Don\'t you go ˙◠˙',
    'Shall we do it again?', 'The cake is a lie.',
    'Yo buddy, you still alive?', 'You dirty old man.',
    'How often do you think about the Roman Empire?',
    'May the Force be with you.', ' ♥ ', 'F',
    'We\'re all doomed.', 'Bye.', 'Nice.',
]

LOGO_MENU = [
    ' ██████╗  █████╗ ████████╗',
    '██╔════╝ ██╔══██╗╚══██╔══╝',
    '██║      ██║  ██║   ██║   ',
    '██║  ███╗██║  ██║   ██║   ',
    '╚██████╔╝╚█████╔╝   ██║   ',
    ' ╚═════╝  ╚════╝    ╚═╝   ',
]

LOGO_MENU_LEN = len(LOGO_MENU)
LOGO_OFFSET = 3

TOP_SWORD = (
    ('blade', '<:::::::::::::::::::::'),
    ('hilt', '}]xxxx)o'),
)

BOTTOM_SWORD = (
    ('hilt', 'o(xxxx[{'),
    ('blade', ':::::'),
    ('other', 'GAMES'),
    ('blade', ':::::::::::>'),
)

MENU_MAX_LEN = TOP_SWORD_LEN = sum([len(part) for _, part in TOP_SWORD])
BOTTOM_SWORD_LEN = sum([len(part) for _, part in TOP_SWORD])

SWORD_COLORS = {
    'blade': 'grey_text_black_bg',
    'hilt': 'very_light_grey_text_black_bg',
    'other': 'very_light_grey_text_black_bg',
}

FIRE_CHARS = [" ", ".", ":", "*", "s", "S", "#", "$"]
FIRE_CHARS_LEN = len(FIRE_CHARS)

# affects on the height of fire
FIRE_ELEMENTS_COUNT = 85
# affects on the amount of fire
AMOUNT_OF_FIRE_DIV = 7

# delay between fire redraw
FIRE_ANIMATION_SPEED = 150

FIRE_COLORS = {
    'Warm Home': {
        15: 'yellow_text_black_bg',
        9: 'red_text_black_bg',
        0: 'light_black_text_black_bg',
    },
    'Cold Dungeon': {
        15: 'light_blue_text_black_bg',
        9: 'dark_medium_blue_text_black_bg',
        0: 'light_black_text_black_bg',
    },
}

CREATOR_NAME = 'by zluuba'
