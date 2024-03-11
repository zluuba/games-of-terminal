from games_of_terminal.constants import TERM_RED_COLOR
from games_of_terminal.menu.core import Menu
from games_of_terminal.utils import init_curses_colors

from curses import (wrapper as curses_wrapper,
                    error as curses_error,
                    endwin)
from sys import exit, stderr


@curses_wrapper
def main(canvas):
    try:
        init_curses_colors()
        menu = Menu(canvas)
        menu.run_menu_loop()

    except (curses_error, Exception) as error:
        message = ('That shouldn\'t have happened, but it is what it is.\n' +
                   TERM_RED_COLOR + f'Curses Error: {error}')
        stderr.write(message)
        endwin()
        exit(1)


if __name__ == '__main__':
    main()
