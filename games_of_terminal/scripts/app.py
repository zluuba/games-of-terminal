from games_of_terminal.menu.core import Menu

from curses import (wrapper as curses_wrapper,
                    error as curses_error,
                    endwin)
from sys import exit, stderr


@curses_wrapper
def main(canvas):
    # try:
    #     menu = Menu(canvas)
    #     menu.run_menu_loop()
    # except curses_error as app_error:
    #     message = f'Oops! Error: {app_error}'
    #     stderr.write(message)
    #     endwin()
    #     exit(1)

    menu = Menu(canvas)
    menu.run_menu_loop()


if __name__ == '__main__':
    main()
