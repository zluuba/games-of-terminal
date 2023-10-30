from games_of_terminal.constants import KEYS, MESSAGES
from games_of_terminal.games.engine import GameEngine

from games_of_terminal.games.snake.constants import *
from games_of_terminal.games.snake.score import (
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
        self.gb_top_border = self.game_box_sizes['begin_y'] - 1
        self.gb_bottom_border = self.game_box_sizes['lines'] - self.gb_top_border - 1
        self.gb_left_border = self.game_box_sizes['begin_x']
        self.gb_right_border = self.game_box_sizes['cols'] - self.gb_left_border - 1

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

    def _setup_game_field(self):
        self.hide_cursor()
        self.window.nodelay(1)
        self.window.timeout(150)

        self._set_score()
        self._put_food_on_the_field()

        self._setup_side_menu()
        self.show_game_status()

    def start_new_game(self):
        self._setup_game_field()

        while True:
            key = self.window.getch()

            if key == KEYS['escape']:
                curses.endwin()
                return
            elif key in DIRECTIONS.keys():
                self._change_direction(key)

            self._move_snake()

            if self._is_snake_eat_itself() or self._is_snake_touch_the_border():
                self.game_status = 'user_lose'
                self.show_game_status()
                self._save_best_score()

                curses.flash()
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
            self.draw_message(3, 1,
                              self.side_menu_box, message,
                              self.get_color_by_name('white_text_green_bg'))
