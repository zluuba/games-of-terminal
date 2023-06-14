import curses
import random
import time
import sys


menu = ['Snake', 'Tic Tac Toe', 'Minesweeper', 'Tetris', 'Unsolicited advice']
goodbye_words = [
    'Already miss you.', 'Where are you going?',
    'Don\'t you go. ˙◠˙', 'Bye.', 'Have a great day!',
    'Nice.', 'Finally.', 'We had a great time!',
    'Shall we do it again?', 'Don\'t forget to rest.', 'Huh.',
]


def show_menu(stdscr, selected_row_ind):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    for ind, item in enumerate(menu):
        x = w // 2 - len(item) // 2
        y = h // 2 - len(menu) // 2 + ind

        if ind == selected_row_ind:
            stdscr.addstr(y, x, item, curses.A_STANDOUT)
        else:
            stdscr.addstr(y, x, item)

    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

    h, w = stdscr.getmaxyx()
    x = w // 2
    y = h // 2

    # set background
    stdscr.bkgd(' ', curses.color_pair(1))

    menu_current_row_ind = 0
    show_menu(stdscr, menu_current_row_ind)

    while True:
        key = stdscr.getch()
        stdscr.clear()

        # 27 - Esc button
        if key == 27:
            goodbye_message = random.choice(goodbye_words)
            stdscr.addstr(y, x - len(goodbye_message) // 2, goodbye_message)
            stdscr.refresh()
            time.sleep(1.5)
            sys.exit(0)

        if key == curses.KEY_UP and menu_current_row_ind > 0:
            menu_current_row_ind -= 1
        elif key == curses.KEY_DOWN and menu_current_row_ind < len(menu) - 1:
            menu_current_row_ind += 1
        elif key in (curses.KEY_ENTER, 10, 13):
            stdscr.addstr(
                y, x - len(menu[menu_current_row_ind]) // 2,
                menu[menu_current_row_ind]
            )
            stdscr.refresh()
            stdscr.getch()

        show_menu(stdscr, menu_current_row_ind)

        stdscr.refresh()

    # stdscr.addstr(y, x, text, curses.color_pair(1) | curses.A_REVERSE)


curses.wrapper(main)
