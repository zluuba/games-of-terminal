from terminal_games.games.snake.constants import *
from terminal_games.games.snake.score import (
    show_score, show_best_score, save_best_score
)
from terminal_games.games.engine import GameEngine

from random import randint
import curses
import time


class SnakeGame(GameEngine):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.score = 0
        self.snake = None
        self.food = None

    def _set_snake(self):
        self.snake = [
            [self.game_box_height // 2, self.game_box_width // 2 + 1],
            [self.game_box_height // 2, self.game_box_width // 2],
            [self.game_box_height // 2, self.game_box_width // 2 - 1]
        ]

    def _get_food_coords(self):
        box = self.sizes['game_box']
        food = [randint(box['begin_y'] + 1, box['lines'] - 1),
                randint(box['begin_x'] + 1, box['cols'] - 1)]

        if food in self.snake:
            return self._get_food_coords()
        return food

    def _set_food(self):
        self.food = self._get_food_coords()
        self.game_box.addstr(*self.food, FOOD_SKIN)

    def _set_score(self):
        show_score(self.canvas, self.score, self.width)
        show_best_score(self.canvas, self.width)

    def _draw_game_field(self):
        curses.curs_set(0)
        self.window.nodelay(1)
        self.window.timeout(150)

        self._set_snake()
        self._set_food()
        self._set_score()

    def start_new_game(self):
        self._draw_game_field()

        direction = curses.KEY_RIGHT

        while True:
            key = self.window.getch()

            if key == KEYS['esc_btn']:
                time.sleep(1)
                curses.endwin()
                return
            elif key in DIRECTIONS.keys():
                direction = key

            self._move_snake(direction)

            top = self.sizes['game_box']['begin_y'] - 1
            bottom = self.sizes['game_box']['lines'] - top - 1
            left = self.sizes['game_box']['begin_x']
            right = self.sizes['game_box']['cols'] - left - 1

            if (self.snake[0][0] in [top, bottom]) or \
               (self.snake[0][1] in [left, right]) or \
               (self.snake[0] in self.snake[1:]):
                curses.flash()

                self._finish_game()
                self._save_best_score()
                time.sleep(1)

                if self._restart_the_game():
                    self.start_new_game()
                return

            self.game_box.refresh()
            self.window.refresh()

    def _move_snake(self, direction):
        snake_head = self.snake[0]

        if direction == KEYS['right_arrow']:
            snake_head = [snake_head[0], snake_head[1] + 1]
        elif direction == KEYS['left_arrow']:
            snake_head = [snake_head[0], snake_head[1] - 1]
        elif direction == KEYS['up_arrow']:
            snake_head = [snake_head[0] - 1, snake_head[1]]
        elif direction == KEYS['down_arrow']:
            snake_head = [snake_head[0] + 1, snake_head[1]]

        self.snake.insert(0, snake_head)
        self.game_box.addstr(*snake_head, SNAKE_SKIN)

        if snake_head == self.food:
            self._set_food()
            self.score += 1
            show_score(self.canvas, self.score, self.width)
        else:
            snake_tail = self.snake.pop()
            self.game_box.addstr(*snake_tail, ' ')

        self.game_box.refresh()

    def _save_best_score(self):
        is_best_score = save_best_score(self.score)
        if is_best_score:
            show_best_score(self.canvas, self.width)
            message = MESSAGES['new_best_score']
            self.canvas.addstr(
                2, (self.width - len(message) - 3),
                message, curses.color_pair(2)
            )
            self.canvas.refresh()

    def _finish_game(self):
        message = MESSAGES['game_over']
        self.game_box.addstr(
            self.game_box_height // 2,
            self.game_box_width // 2 - len(message) // 2,
            message, curses.color_pair(8),
        )
        self.game_box.nodelay(0)
        self.game_box.refresh()

    def _restart_the_game(self):
        message = MESSAGES['play_again']
        self.game_box.addstr(
            self.game_box_height // 2 + 2,
            self.game_box_width // 2 - len(message) // 2,
            message, curses.A_BLINK
        )
        self.game_box.refresh()

        curses.flushinp()
        self._wait()
        key = self.window.getch()

        if key == KEYS['space_btn']:
            self.game_box.clear()
            self.game_box.border()
            return True
        return False
