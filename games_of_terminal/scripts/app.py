from games_of_terminal.menu.core import Menu
import curses
import sys


@curses.wrapper
def main(canvas):
    try:
        menu = Menu(canvas)
        menu.run_menu_loop()
    except curses.error as app_error:
        message = f'Oops! Error: {app_error}'
        sys.stderr.write(message)
        sys.exit(1)


if __name__ == '__main__':
    main()
