from games_of_terminal.constants import KEYS
from games_of_terminal.utils import hide_cursor
from games_of_terminal.games.engine import GameEngine
from games_of_terminal.games.snake.constants import (
    GAME_TIPS, DIRECTIONS, SNAKE_SKIN, FOOD_SKIN,
)
# from games_of_terminal.database.database import (
#     get_game_state,
#     update_game_state,
# )

from random import randint


class SnakeGame(GameEngine):
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

    def setup_game_field(self):
        hide_cursor()
        self.window.nodelay(1)
        self.window.timeout(150)

        self._put_food_on_the_field()
        self.set_best_score()

        self.draw_logo()
        self.show_game_status()
        self.show_side_menu_tips(
            game_state=self.tips,
            game_tips=GAME_TIPS,
        )

    def start_new_game(self):
        while True:
            key = self.window.getch()
            self.controller(key)

            if self.stats.is_exit or self.stats.is_restart:
                return
            if self.is_game_over():
                self._save_best_score()
                self.ask_for_restart()
                return

            self._move_snake()

            if self._is_snake_eat_itself() or self._is_snake_touch_the_border():
                self.stats.game_status = 'user_lose'

    def controller(self, key, pause_off=False):
        super().controller(key, pause_off)

        if key in DIRECTIONS.keys():
            self._change_direction(key)

    def set_best_score(self):
        pass
        # data = get_game_state('Snake', 'best_score')
        # self.stats.best_score = data

    @property
    def tips(self):
        return {
            'Score': self.stats.score,
            'Best Score': self.stats.best_score,
        }

    def _get_food_coords(self):
        food = [randint(self.game_area.top_border + 1, self.game_area.bottom_border - 1),
                randint(self.game_area.left_border + 1, self.game_area.right_border - 1)]

        if food in self.snake:
            return self._get_food_coords()
        return food

    def _put_food_on_the_field(self):
        self.food = self._get_food_coords()
        self.game_area.box.addstr(*self.food, FOOD_SKIN)

    def _change_direction(self, chosen_direction):
        opposite_direction = DIRECTIONS[self.direction]

        if chosen_direction != opposite_direction:
            self.direction = chosen_direction

    def _is_snake_eat_itself(self):
        return self.snake[0] in self.snake[1:]

    def _is_snake_touch_the_border(self):
        return (self.snake[0][0] in [self.game_area.top_border, self.game_area.bottom_border]) or \
               (self.snake[0][1] in [self.game_area.left_border, self.game_area.right_border])

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
        self.game_area.box.addstr(*snake_head, SNAKE_SKIN)

        if snake_head == self.food:
            self.stats.score += 1
            self._put_food_on_the_field()
            self.show_side_menu_tips(
                game_state=self.tips,
                game_tips=GAME_TIPS,
            )
        else:
            snake_tail = self.snake.pop()
            self.game_area.box.addstr(*snake_tail, ' ')

        self.game_area.box.refresh()

    def _save_best_score(self):
        if self.stats.score <= self.stats.best_score:
            return

        # update_game_state(
        #     'Snake', 'best_score',
        #     self.stats.score, save_mode=True
        # )
