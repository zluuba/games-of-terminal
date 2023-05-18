from terminal_games.games.snake.core import SnakeGame
import curses


@curses.wrapper
def main(canvas):
    game = SnakeGame(canvas)
    game.start_new_game()


if __name__ == '__main__':
    main()
