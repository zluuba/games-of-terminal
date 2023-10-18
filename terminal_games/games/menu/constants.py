from terminal_games.games.snake.core import SnakeGame
from terminal_games.games.minesweeper.core import MinesweeperGame
from terminal_games.games.tictactoe.core import TicTacToeGame
from terminal_games.games.tetris.core import TetrisGame


GAMES = {
    1: {'name': 'Snake', 'game': SnakeGame},
    2: {'name': 'Minesweeper', 'game': MinesweeperGame},
    3: {'name': 'Tic Tac Toe', 'game': TicTacToeGame},
    4: {'name': 'Tetris', 'game': TetrisGame},
}

GOODBYE_MESSAGES = [
    'Already miss you.', 'You\'re a geek, right?',
    'Have a great day, babe', 'Don\'t you go ˙◠˙',
    'Shall we do it again?', 'The cake is a lie.',
    'Yo buddy, you still alive?', 'You dirty old man.',
    'How often do you think about the Roman Empire?',
    'May the Force be with you.', ' ♥ ', 'F',
    'We\'re all doomed.', 'Bye.', 'Nice.',
]
