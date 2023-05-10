from curses import textpad
import curses
import random
import os


CURSES_DIRECTIONS = [
    curses.KEY_RIGHT, curses.KEY_LEFT,
    curses.KEY_UP, curses.KEY_DOWN,
]

OPPOSITE_DIRECTIONS = {
    curses.KEY_RIGHT: curses.KEY_LEFT, curses.KEY_LEFT: curses.KEY_RIGHT,
    curses.KEY_UP: curses.KEY_DOWN, curses.KEY_DOWN: curses.KEY_UP,
}

MESSAGES = {
    'game_over': 'GAME OVER',
    'score_text': 'Score: ',
    'best_score': 'Best score: ',
    'new_best_score': 'New best score!',
}


def create_food(snake, box):
    while True:
        food = [
            random.randint(box[0][0] + 1, box[1][0] - 1),
            random.randint(box[0][1] + 1, box[1][1] - 1)
        ]

        if food not in snake:
            return food


def print_score(stdscr, score):
    _, sw = stdscr.getmaxyx()
    score_text = MESSAGES['score_text'] + str(score)
    stdscr.addstr(1, sw // 2 - len(score_text) // 2, score_text)


def print_best_score(stdscr):
    _, sw = stdscr.getmaxyx()
    filename = 'best_score.txt'
    directory = os.getcwd()
    file_path = os.path.join(directory, filename)
    best_score = open(file_path, 'r').read()
    best_score_text = MESSAGES['best_score'] + str(best_score)
    stdscr.addstr(1, sw - len(best_score_text) - 3, best_score_text)


def save_best_score(score):
    filename = 'best_score.txt'
    directory = os.getcwd()
    file_path = os.path.join(directory, filename)
    best_score = open(file_path, 'r').read()
    if score > int(best_score):
        open(file_path, 'w').write(str(score))
        return True
    return False


def engine(stdscr):
    curses.curs_set(0)

    # for not waiting for user
    # change this to "press any key to start"
    stdscr.nodelay(1)
    stdscr.timeout(150)

    # sh, sm - screen height, screen width
    # getmaxyx - get current screen height and width
    sh, sw = stdscr.getmaxyx()

    box = [[3, 3], [sh - 3, sw - 3]]

    # create rectangle
    textpad.rectangle(stdscr, *box[0], *box[1])

    # define snake
    snake = [[sh // 2, sw // 2 + 1], [sh // 2, sw // 2], [sh // 2, sw // 2 - 1]]
    direction = curses.KEY_RIGHT

    # draw snake
    for x, y in snake:
        stdscr.addstr(x, y, '#')

    # add food on screen
    food = create_food(snake, box)
    stdscr.addstr(food[0], food[1], '*')

    # print scores
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
        stdscr.addstr(new_head[0], new_head[1], '#')

        if snake[0] == food:
            food = create_food(snake, box)
            stdscr.addstr(food[0], food[1], '*')

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
            is_best_score = save_best_score(score)
            if is_best_score:
                message = MESSAGES['new_best_score']
                stdscr.addstr(sh // 2 + 1, sw // 2 - len(message) // 2, message)

            message = MESSAGES['game_over']
            stdscr.addstr(sh // 2, sw // 2 - len(message) // 2, message)
            stdscr.nodelay(0)
            stdscr.getch()
            break

        stdscr.refresh()


curses.wrapper(engine)
