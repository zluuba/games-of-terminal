from terminal_games.games.tictactoe.core import TicTacToeGame
import curses


@curses.wrapper
def main(canvas):
    game = TicTacToeGame(canvas)
    game.start_new_game()


if __name__ == '__main__':
    main()
