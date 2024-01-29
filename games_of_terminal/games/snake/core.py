from games_of_terminal.constants import KEYS
from games_of_terminal.database.database import get_game_stat_value
from games_of_terminal.games.engine import GameEngine
from games_of_terminal.log import log
from games_of_terminal.games.snake.constants import (
    GAME_TIPS, DIRECTIONS, SNAKE_SKIN, FOOD_SKIN,
)
from games_of_terminal.utils import (
    hide_cursor,
    update_total_time_count,
    update_total_games_count,
    update_best_score,
    draw_message,
)

from random import randint
from time import time


class SnakeGame(GameEngine):
    @log
    def setup_game_stats(self):
        # initial position of the snake:
        # placed in the center of the game box, have 3 sections [y, x]
        self.snake = [
            [self.game_area.height // 2, self.game_area.width // 2 + 1],
            [self.game_area.height // 2, self.game_area.width // 2],
            [self.game_area.height // 2, self.game_area.width // 2 - 1]
        ]

        # initial direction of the snake's movement
        self.direction = KEYS['right_arrow']
        self.food = None

        self.start_time = time()

    @log
    def setup_game_field(self):
        hide_cursor()
        self.window.nodelay(1)
        self.window.timeout(150)

        self.put_food_on_the_field()
        self.set_best_score()

        self.draw_game_window()
        self.draw_side_menu_logo()
        self.show_game_status()
        self.show_side_menu_tips(
            game_state=self.tips,
            game_tips=GAME_TIPS,
        )

    @log
    def start_new_game(self):
        while True:
            key = self.window.getch()

            if key != -1:
                self.controller(key)

            if self.stats.is_exit or self.stats.is_restart:
                self.save_game_data()
                return
            if self.is_game_over():
                self.save_game_data()
                self.ask_for_restart()
                return

            self.move_snake()

            if self.is_snake_eat_itself() or self.is_snake_touch_the_border():
                self.stats.game_status = 'user_lose'

    def draw_game_window(self):
        self.game_area.box.erase()
        self.game_area.show_borders()

        if self.food:
            draw_message(*self.food, self.game_area.box, FOOD_SKIN)

        if self.snake:
            for y, x in self.snake:
                draw_message(y, x, self.game_area.box, SNAKE_SKIN)

    def controller(self, key, pause_on=True):
        super().controller(key, pause_on)

        if key in DIRECTIONS.keys():
            self.change_direction(key)

    @log
    def set_best_score(self):
        data = get_game_stat_value('Snake', 'best_score')
        self.stats.best_score = int(data)

    @property
    def tips(self):
        return {
            'Score': self.stats.score,
            'Best Score': self.stats.best_score,
        }

    def get_food_coords(self):
        food_y = randint(
            self.game_area.top_border + 1,
            self.game_area.bottom_border - 1,
        )
        food_x = randint(
            self.game_area.left_border + 1,
            self.game_area.right_border - 1,
        )
        food = [food_y, food_x]

        if food in self.snake:
            return self.get_food_coords()
        return food

    def put_food_on_the_field(self):
        self.food = self.get_food_coords()
        draw_message(*self.food, self.game_area.box, FOOD_SKIN)

    def change_direction(self, chosen_direction):
        opposite_direction = DIRECTIONS[self.direction]

        if chosen_direction != opposite_direction:
            self.direction = chosen_direction

    def is_snake_eat_itself(self):
        return self.snake[0] in self.snake[1:]

    def is_snake_touch_the_border(self):
        return (self.snake[0][0] in [self.game_area.top_border,
                                     self.game_area.bottom_border]) or \
               (self.snake[0][1] in [self.game_area.left_border,
                                     self.game_area.right_border])

    def move_snake(self):
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
        draw_message(*snake_head, self.game_area.box, SNAKE_SKIN)

        if snake_head == self.food:
            self.stats.score += 1
            self.put_food_on_the_field()
            self.show_side_menu_tips(
                game_state=self.tips,
                game_tips=GAME_TIPS,
            )
        else:
            snake_tail = self.snake.pop()
            empty_space = ' '
            draw_message(*snake_tail, self.game_area.box, empty_space)

        self.game_area.box.refresh()

    @log
    def save_game_data(self):
        update_total_games_count(self.game_name, 1)
        update_total_time_count(self.game_name, self.start_time)

        if self.stats.score > self.stats.best_score:
            update_best_score(self.game_name, self.stats.score)
