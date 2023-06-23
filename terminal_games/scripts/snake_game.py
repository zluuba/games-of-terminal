from terminal_games.games.snake.core import SnakeGame


def start_snake_game(canvas):
    game = SnakeGame(canvas)
    game.start_new_game()
