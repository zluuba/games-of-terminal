""" for experiments """

import curses
import sys


def main(canvas):
    curses.curs_set(0)
    curses.mousemask(1)

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)

    # height, width = canvas.getmaxyx()

    # nlines, ncols, begin_y, begin_x
    window = curses.newwin(10, 15, 2, 2)
    window.nodelay(True)
    window.keypad(True)
    window.border()

    while True:
        key = window.getch()

        if key == curses.KEY_MOUSE:
            _, x, y, _, _ = curses.getmouse()

            if 2 <= x <= 17 and 2 <= y <= 12:
                window.addstr(2, 2, f'x: {x}, y: {y}', curses.color_pair(1))
            else:
                window.addstr(2, 2, f'x: {x}, y: {y}', curses.color_pair(2))

        if key == 27:
            sys.exit(0)


if __name__ == "__main__":
    curses.wrapper(main)
