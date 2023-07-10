from terminal_games.games.tetris.core import TetrisGame


def start_tetris_game(canvas):
    game = TetrisGame(canvas)
    game.start_new_game()
