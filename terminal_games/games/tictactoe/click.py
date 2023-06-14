import curses


def main(stdscr):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)

    stdscr.addstr(0, 0, 'Such Wow')

    red = 'Red'
    green = 'Green'

    stdscr.addstr(1, 0, red)
    stdscr.addstr(2, 0, green)

    curses.curs_set(0)
    curses.mousemask(1)

    while True:
        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_MOUSE:
            _, x, y, _, _ = curses.getmouse()

            if y == 1 and x in range(len(red)):
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(0, 0, 'Such Wow')
                stdscr.attroff(curses.color_pair(1))

            elif y == 2 and x in range(len(green)):
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(0, 0, 'Such Wow')
                stdscr.attroff(curses.color_pair(2))

        elif key == 27:
            break


curses.wrapper(main)
