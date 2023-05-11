from common import CURSES_DIRECTIONS, OPPOSITE_DIRECTIONS, MESSAGES
from score import print_score, print_best_score, save_best_score
from food import create_food
from curses import textpad
import curses
import time


GAMES = 0
SNAKE_SKIN = '#'
FOOD_SKIN = '*'


def engine(stdscr):
    """
    rebuild this function on class
    """

    curses.curs_set(0)

    # get current screen height and width, create rectangle
    sh, sw = stdscr.getmaxyx()
    box = [[3, 3], [sh - 3, sw - 3]]
    textpad.rectangle(stdscr, *box[0], *box[1])

    while True:
        global GAMES
        if GAMES > 0:
            break

        message = MESSAGES['start_text']
        stdscr.addstr(sh // 2, sw // 2 - len(message) // 2, message)

        if stdscr.getch():
            spaces = ' ' * len(message)
            stdscr.addstr(sh // 2, sw // 2 - len(message) // 2, spaces)
            break

    # for not waiting for user
    # change this to "press any key to start"
    stdscr.nodelay(1)
    stdscr.timeout(150)

    # define snake
    snake = [[sh // 2, sw // 2 + 1], [sh // 2, sw // 2], [sh // 2, sw // 2 - 1]]
    direction = curses.KEY_RIGHT

    # draw snake
    for x, y in snake:
        stdscr.addstr(x, y, SNAKE_SKIN)

    food = create_food(snake, box)
    stdscr.addstr(food[0], food[1], FOOD_SKIN)

    score = 0
    print_score(stdscr, score)
    print_best_score(stdscr)

    while True:
        # key - user input
        key = stdscr.getch()
        if key in CURSES_DIRECTIONS:
            if direction == OPPOSITE_DIRECTIONS[key]:
                continue
            direction = key

        snake_head = snake[0]
        new_head = None

        if direction == curses.KEY_RIGHT:
            new_head = [snake_head[0], snake_head[1] + 1]
        elif direction == curses.KEY_LEFT:
            new_head = [snake_head[0], snake_head[1] - 1]
        elif direction == curses.KEY_UP:
            new_head = [snake_head[0] - 1, snake_head[1]]
        elif direction == curses.KEY_DOWN:
            new_head = [snake_head[0] + 1, snake_head[1]]

        if new_head:
            snake.insert(0, new_head)
        stdscr.addstr(new_head[0], new_head[1], SNAKE_SKIN)

        if snake[0] == food:
            food = create_food(snake, box)
            stdscr.addstr(food[0], food[1], FOOD_SKIN)

            score += 1
            print_score(stdscr, score)

        else:
            stdscr.addstr(snake[-1][0], snake[-1][1], ' ')
            snake.pop()

        # game over conditions
        # if snake touch any box border (1, 2)
        # if snake touch herself (3)
        if (snake[0][0] in [box[0][0], box[1][0]]) or \
                (snake[0][1] in [box[0][1], box[1][1]]) or \
                (snake[0] in snake[1:]):
            curses.flash()

            is_best_score = save_best_score(score)
            if is_best_score:
                message = MESSAGES['new_best_score']
                stdscr.addstr(sh // 3, sw // 2 - len(message) // 2, message)

            message = MESSAGES['game_over']
            stdscr.addstr(sh // 2, sw // 2 - len(message) // 2, message)
            stdscr.nodelay(0)
            stdscr.refresh()

            time.sleep(1)
            message = MESSAGES['play_again']
            stdscr.addstr(sh // 2 + 2, sw // 2 - len(message) // 2, message, curses.A_BLINK)

            curses.flushinp()
            key = stdscr.getch()
            if key == ord(' '):
                GAMES += 1
                stdscr.clear()
                curses.wrapper(engine)
            return

        stdscr.refresh()


curses.wrapper(engine)
