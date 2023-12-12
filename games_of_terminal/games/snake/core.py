from games_of_terminal.constants import KEYS, MESSAGES
from games_of_terminal.games.engine import GameEngine

from games_of_terminal.games.snake.constants import *
from games_of_terminal.database.database import get_game_state, save_game_state

from random import randint


class SnakeGame(GameEngine):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.score = 0
        self.best_score = 0
        self.food = None

        # initial position of the snake:
        # placed in the center of the game box, have 3 sections [y, x]
        self.snake = [
            [self.game_area.height // 2, self.game_area.width // 2 + 1],
            [self.game_area.height // 2, self.game_area.width // 2],
            [self.game_area.height // 2, self.game_area.width // 2 - 1]
        ]

        # initial direction of the snake's movement
        self.direction = KEYS['right_arrow']

    def start_new_game(self):
        self._setup_game_field()
        self.draw_game_tips(self.tips)

        while True:
            key = self.window.getch()
            self.controller(key)

            if self.is_exit:
                return
            if self.is_game_over():
                self._save_best_score()
                is_restart = self.ask_for_restart()
                if not is_restart:
                    return

            self._move_snake()

            if self._is_snake_eat_itself() or self._is_snake_touch_the_border():
                self.game_status = 'user_lose'
                if not self.is_game_over():
                    return

            self.game_area.box.refresh()
            self.window.refresh()

    def controller(self, key, pause_off=False):
        super().controller(key, pause_off)

        if key in DIRECTIONS.keys():
            self._change_direction(key)

    def set_best_score(self):
        data = get_game_state('Snake', 'best_score')
        self.best_score = data

    @property
    def tips(self):
        return {
            'Score': self.score,
            'Best Score': self.best_score,
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

    def _setup_game_field(self):
        self.hide_cursor()
        self.window.nodelay(1)
        self.window.timeout(150)

        self._put_food_on_the_field()

        self.setup_side_menu()
        self.show_game_status()

        self.set_best_score()

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
            self.score += 1
            self._put_food_on_the_field()
            self.draw_game_tips(self.tips)
        else:
            snake_tail = self.snake.pop()
            self.game_area.box.addstr(*snake_tail, ' ')

        self.game_area.box.refresh()

    def _save_best_score(self):
        if self.score > self.best_score:
            save_game_state('Snake', 'best_score', self.score)

            message = MESSAGES['new_best_score']
            self.draw_message(9, 2,
                              self.tips_area.box, message,
                              self.get_color_by_name('white_text_green_bg'))
