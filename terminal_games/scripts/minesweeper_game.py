from terminal_games.games.minesweeper.core import MinesweeperGame


def start_minesweeper_game(canvas):
    game = MinesweeperGame(canvas)
    game.start_new_game()
