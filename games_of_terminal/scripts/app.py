from games_of_terminal.games.menu.core import Menu
import curses


@curses.wrapper
def main(canvas):
    menu = Menu(canvas)
    menu.run_menu_loop()


if __name__ == '__main__':
    main()
