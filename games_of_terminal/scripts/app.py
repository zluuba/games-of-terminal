from games_of_terminal.constants import (
    TERM_DEFAULT_COLOR, TERM_RED_COLOR, ERROR_MSG,
)
from games_of_terminal.menu.core import Menu
from games_of_terminal.utils import init_curses_colors

from curses import (wrapper as curses_wrapper,
                    error as curses_error)
from sys import exit, platform
from subprocess import run as run_bash_cmd


@curses_wrapper
def main(canvas):
    if platform == 'linux':
        run_bash_cmd('TERM=xterm-256color', shell=True)

    try:
        init_curses_colors()
        menu = Menu(canvas)
        menu.run_menu_loop()
        exit(0)
    except (curses_error, Exception) as error:
        message = (ERROR_MSG + '\n' +
                   TERM_RED_COLOR + f'{error.__class__}: {error}' +
                   TERM_DEFAULT_COLOR)
        exit(message)
        # raise error


if __name__ == '__main__':
    main()
