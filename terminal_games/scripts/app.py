from terminal_games.games.menu import Menu
import curses


@curses.wrapper
def main(canvas):
    menu = Menu(canvas)
    menu.main()


if __name__ == '__main__':
    main()
