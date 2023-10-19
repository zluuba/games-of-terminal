from terminal_games.games.constants import KEYS, MESSAGES
from terminal_games.games.engine import GameEngine

from terminal_games.games.snake.constants import *
from terminal_games.games.snake.score import (
    show_score, show_best_score, save_best_score
)

from random import randint
import curses
import time


class SnakeGame(GameEngine):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.score = 0
        self.food = None

        # initial position of the snake:
        # placed in the center of the game box, have 3 sections [y, x]
        self.snake = [
            [self.game_box_height // 2, self.game_box_width // 2 + 1],
            [self.game_box_height // 2, self.game_box_width // 2],
            [self.game_box_height // 2, self.game_box_width // 2 - 1]
        ]

        # initial direction of the snake's movement:
        # by default it crawls to the right
        self.direction = KEYS['right_arrow']

        # game box borders
        gb_sizes = self.sizes['game_box']
        self.gb_top_border = gb_sizes['begin_y'] - 1
        self.gb_bottom_border = gb_sizes['lines'] - self.gb_top_border - 1
        self.gb_left_border = gb_sizes['begin_x']
        self.gb_right_border = self.sizes['game_box']['cols'] - self.gb_left_border - 1

    def _set_score(self):
        show_score(self.side_menu_box, self.score, self.side_menu_box_width)
        show_best_score(self.side_menu_box, self.side_menu_box_width)

    def _get_food_coords(self):
        food = [randint(self.gb_top_border + 1, self.gb_bottom_border - 1),
                randint(self.gb_left_border + 1, self.gb_right_border - 1)]

        if food in self.snake:
            return self._get_food_coords()
        return food

    def _put_food_on_the_field(self):
        self.food = self._get_food_coords()
        self.game_box.addstr(*self.food, FOOD_SKIN)

    def _draw_game_field(self):
        curses.curs_set(0)
        self.window.nodelay(1)
        self.window.timeout(150)

        self._set_score()
        self._put_food_on_the_field()

    def start_new_game(self):
        self._draw_game_field()

        while True:
            key = self.window.getch()

            if key == KEYS['escape']:
                curses.endwin()
                return
            # elif key == KEYS['p']:
                # self._pause()
                # continue
            elif key in DIRECTIONS.keys():
                self._change_direction(key)

            self._move_snake()

            if self._is_snake_eat_itself() or self._is_snake_touch_the_border():
                curses.flash()

                self._draw_game_over_message()
                self._save_best_score()
                time.sleep(1)

                if self._is_restart():
                    self.__init__(self.canvas)
                    self.start_new_game()
                return

            self.game_box.refresh()
            self.window.refresh()

    def _change_direction(self, chosen_direction):
        opposite_direction = DIRECTIONS[self.direction]

        if chosen_direction != opposite_direction:
            self.direction = chosen_direction

    def _is_snake_eat_itself(self):
        return self.snake[0] in self.snake[1:]

    def _is_snake_touch_the_border(self):
        return (self.snake[0][0] in [self.gb_top_border, self.gb_bottom_border]) or \
               (self.snake[0][1] in [self.gb_left_border, self.gb_right_border])

    def _move_snake(self):
        snake_head = self.snake[0]

        if self.direction == KEYS['right_arrow']:
            snake_head = [snake_head[0], snake_head[1] + 1]
        elif self.direction == KEYS['left_arrow']:
            snake_head = [snake_head[0], snake_head[1] - 1]
        elif self.direction == KEYS['up_arrow']:
            snake_head = [snake_head[0] - 1, snake_head[1]]
        elif self.direction == KEYS['down_arrow']:
            snake_head = [snake_head[0] + 1, snake_head[1]]

        self.snake.insert(0, snake_head)
        self.game_box.addstr(*snake_head, SNAKE_SKIN)

        if snake_head == self.food:
            self.score += 1
            self._set_score()
            self._put_food_on_the_field()
        else:
            snake_tail = self.snake.pop()
            self.game_box.addstr(*snake_tail, ' ')

        self.game_box.refresh()

    def _save_best_score(self):
        is_best_score = save_best_score(self.score)

        if is_best_score:
            show_best_score(self.side_menu_box, self.side_menu_box_width)
            message = MESSAGES['new_best_score']
            self.side_menu_box.addstr(
                3, (self.side_menu_box_width // 2 - len(message) // 2),
                message, curses.color_pair(2)
            )
            self.side_menu_box.refresh()

    def _is_restart(self):
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

        if key == KEYS['space']:
            self.game_box.erase()
            return True
        return False
