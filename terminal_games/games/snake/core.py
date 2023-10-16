from terminal_games.games.snake.constants import *
from terminal_games.games.snake.food import create_food
from terminal_games.games.snake.score import (
    show_score, show_best_score, save_best_score
)

from curses import textpad

import curses
import time


class GameEngine:
    def set_game_area(self, top, bottom, left, right):
        self.box = [[top, bottom],
                    [self.screen_height - left, self.screen_width - right]]
        # get rid of textpad lib, rebuild it with curses
        textpad.rectangle(self.canvas, *self.box[0], *self.box[1])

    @staticmethod
    def set_colors():
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)


class SnakeGame(GameEngine):
    def __init__(self, canvas):
        self.screen_height, self.screen_width = canvas.getmaxyx()
        self.canvas = canvas
        self.box = []

        self.snake = []
        self.food = []

        self.score = 0
        self.games_count = 0

    def set_snake(self):
        self.snake = [
            [self.screen_height // 2, self.screen_width // 2 + 1],
            [self.screen_height // 2, self.screen_width // 2],
            [self.screen_height // 2, self.screen_width // 2 - 1]
        ]

        for x, y in self.snake:
            self.canvas.addstr(x, y, SNAKE_SKIN)

    def put_food(self):
        self.food = create_food(self.snake, self.box)
        self.canvas.addstr(self.food[0], self.food[1], FOOD_SKIN)

    def score_init(self):
        self.score = 0
        show_score(self.canvas, self.score, self.screen_width)
        show_best_score(self.canvas, self.screen_width)

    def start_new_game(self):
        curses.curs_set(0)

        self.set_colors()
        self.canvas.bkgd(' ', curses.color_pair(3))
        self.set_game_area(3, 3, 2, 3)

        self.canvas.nodelay(1)
        self.canvas.timeout(150)

        self.set_snake()
        self.put_food()
        self.score_init()

        while self.engine():
            self.start_new_game()
        return

    def engine(self):
        direction = curses.KEY_RIGHT

        while True:
            key = self.canvas.getch()
            if key == 27:
                time.sleep(1)
                curses.endwin()
                return
            if key in DIRECTIONS.keys():
                if direction == DIRECTIONS[key]:
                    continue
                direction = key

            snake_head = self.snake[0]
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
                self.snake.insert(0, new_head)
            self.canvas.addstr(
                new_head[0], new_head[1], SNAKE_SKIN
            )

            if self.snake[0] == self.food:
                self.food = create_food(self.snake, self.box)
                self.canvas.addstr(
                    self.food[0], self.food[1], FOOD_SKIN
                )

                self.score += 1
                show_score(self.canvas, self.score, self.screen_width)

            else:
                self.canvas.addstr(self.snake[-1][0], self.snake[-1][1], ' ')
                self.snake.pop()

            if (self.snake[0][0] in [self.box[0][0], self.box[1][0]]) or \
                    (self.snake[0][1] in [self.box[0][1], self.box[1][1]]) or \
                    (self.snake[0] in self.snake[1:]):
                curses.flash()

                is_best_score = save_best_score(self.score)
                if is_best_score:
                    show_best_score(self.canvas, self.screen_width)
                    message = MESSAGES['new_best_score']
                    self.canvas.addstr(
                        2, (self.screen_width - len(message) - 3),
                        message, curses.color_pair(2)
                    )
                    self.canvas.refresh()

                message = MESSAGES['game_over']
                self.canvas.addstr(
                    self.screen_height // 2,
                    (self.screen_width // 2 - len(message) // 2),
                    message, curses.color_pair(1),
                )
                self.canvas.nodelay(0)
                self.canvas.refresh()

                time.sleep(1)
                message = MESSAGES['play_again']
                self.canvas.addstr(
                    self.screen_height // 2 + 2,
                    self.screen_width // 2 - len(message) // 2,
                    message, curses.A_BLINK
                )

                curses.flushinp()
                key = self.canvas.getch()
                if key == ord(' '):
                    self.games_count += 1
                    self.canvas.clear()
                    return True
                return False

            self.canvas.refresh()
