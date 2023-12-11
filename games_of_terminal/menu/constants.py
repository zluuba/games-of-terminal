from games_of_terminal.games.snake.core import SnakeGame
from games_of_terminal.games.minesweeper.core import MinesweeperGame
from games_of_terminal.games.tictactoe.core import TicTacToeGame
from games_of_terminal.games.tetris.core import TetrisGame


GAMES = {
    0: {'name': 'Tetris', 'game': TetrisGame},
    1: {'name': 'Minesweeper', 'game': MinesweeperGame},
    2: {'name': 'Tic Tac Toe', 'game': TicTacToeGame},
    3: {'name': 'Snake', 'game': SnakeGame},
    # 4: {'name': 'Settings', 'game': Settings},
}

LOGO_MENU = [
    ' ####     #####   ######',
    '##       ##   ##    ##  ',
    '##  ###  ##   ##    ##  ',
    '##   ##  ##   ##    ##  ',
    ' #####    #####     ##  ',
]
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
SWORD_COLORS = {
    'blade': 'grey_text_black_bg',
    'hilt': 'very_light_grey_text_black_bg',
    'other': 'light_grey_text_black_bg',
}
CREATOR_NAME = 'by zluuba'

GOODBYE_MESSAGES = [
    'Already miss you.', 'You\'re a geek, right?',
    'Have a great day, babe', 'Don\'t you go ˙◠˙',
    'Shall we do it again?', 'The cake is a lie.',
    'Yo buddy, you still alive?', 'You dirty old man.',
    'How often do you think about the Roman Empire?',
    'May the Force be with you.', ' ♥ ', 'F',
    'We\'re all doomed.', 'Bye.', 'Nice.',
]
