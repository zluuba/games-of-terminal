from terminal_games.games.tictactoe.core import TicTacToeGame


def start_tictactoe_game(canvas):
    game = TicTacToeGame(canvas)
    game.start_new_game()
