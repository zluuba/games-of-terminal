from games_of_terminal.constants import KEYS
from games_of_terminal.database.database import (
    get_game_stat_value, get_game_settings,
)
from games_of_terminal.games.engine import GameEngine
from games_of_terminal.log import log
from games_of_terminal.utils import (
    hide_cursor,
    update_total_time_count,
    update_total_games_count,
    update_best_score,
    draw_message,
    get_color_by_name,
    get_current_color_scheme_name,
)

from .achievements_manager import SnakeGameAchievementsManager
from .constants import GAME_TIPS, DIRECTIONS, OBSTACLES_SKINS, COLORS

from random import choice, randint
from time import time


class SnakeGame(GameEngine):
    @log
    def setup_game_stats(self):
        self.snake = []
        self.food = []
        self.obstacles = []

        game_settings = get_game_settings(self.game_name)
        color_scheme = get_current_color_scheme_name(
            game_settings['color_schemes']
        )
        snake_color_name = COLORS[color_scheme]['snake']
        food_color_name = COLORS[color_scheme]['food']
        obstacles_color_name = COLORS[color_scheme]['obstacles']

        self.snake_skin = self.get_selected_skin(game_settings['snake_skins'])
        self.food_skin = self.get_selected_skin(game_settings['food_skins'])

        self.snake_color = get_color_by_name(snake_color_name)
        self.food_color = get_color_by_name(food_color_name)
        self.obstacles_color = get_color_by_name(obstacles_color_name)

        self.snake = self.get_initial_snake()
        self.food = self.get_food_coords()
        self.direction = KEYS['right_arrow']

        self.mode = self.get_selected_mode(game_settings['modes'])
        self.obstacles = self.get_obstacles()

        self.start_time = time()
        self.achievement_manager = SnakeGameAchievementsManager(self)

    def get_initial_snake(self):
        middle_y = self.game_area.height // 2
        middle_x = self.game_area.width // 2

        return [[middle_y, middle_x + 1],
                [middle_y, middle_x],
                [middle_y, middle_x - 1]]

    @staticmethod
    def get_selected_skin(skins):
        for skin in skins:
            if skin['selected']:
                return skin['skin']

    @staticmethod
    def get_selected_mode(modes):
        for mode in modes:
            if mode['selected']:
                return mode['name']

    def get_obstacles(self):
        obstacles = []
        obstacles_count = 10

        if self.mode != 'Obstacles':
            return obstacles

        while obstacles_count:
            y = randint(self.game_area.top_border + 2,
                        self.game_area.bottom_border - 2)
            x = randint(self.game_area.left_border + 2,
                        self.game_area.right_border - 2)
            obstacle = [y, x]

            if (obstacle in self.snake) or \
                    (obstacle == self.food) or \
                    (obstacle in self.get_all_obstacles_coords(obstacles)):
                continue

            obstacle_skin = choice(OBSTACLES_SKINS)
            obstacles.append((obstacle, obstacle_skin))
            obstacles_count -= 1

        return obstacles

    def get_all_obstacles_coords(self, obstacles=None):
        if obstacles is None:
            obstacles = self.obstacles

        return list(map(lambda obs: obs[0], obstacles))

    @log
    def setup_game_field(self):
        hide_cursor()
        self.window.nodelay(1)
        self.window.timeout(150)

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

            if self.is_user_press_key(key):
                self.controller(key)

            if self.stats.is_exit or self.stats.is_restart:
                self.save_game_data()
                self.achievement_manager.check()
                return
            if self.is_game_over():
                self.save_game_data()
                self.achievement_manager.check()
                self.ask_for_restart()
                return

            self.move_snake()

            if self.is_snake_eat_itself() or self.is_snake_touch_the_border():
                self.achievement_manager.check()
                self.stats.game_status = 'user_lose'

    @staticmethod
    def is_user_press_key(key):
        return key != -1

    def draw_game_window(self):
        self.game_area.box.erase()
        self.game_area.show_borders()

        self.put_snake_on_field()
        self.put_food_on_field()
        self.put_obstacles_on_field()

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

        if (food in self.snake) or (food in self.get_all_obstacles_coords()):
            return self.get_food_coords()
        return food

    def put_snake_on_field(self):
        if not self.snake:
            return

        for y, x in self.snake:
            draw_message(y, x, self.game_area.box,
                         self.snake_skin, self.snake_color)

    def put_food_on_field(self):
        if not self.food:
            self.food = self.get_food_coords()

        draw_message(*self.food, self.game_area.box,
                     self.food_skin, self.food_color)

    def put_obstacles_on_field(self):
        if not self.obstacles:
            return

        for obstacle_coords, obstacle_skin in self.obstacles:
            draw_message(*obstacle_coords, self.game_area.box,
                         obstacle_skin, self.obstacles_color)

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
        draw_message(*snake_head, self.game_area.box,
                     self.snake_skin, self.snake_color)

        obstacles = self.get_all_obstacles_coords()

        if snake_head == self.food:
            self.handle_snake_eat_food()
        elif snake_head in obstacles:
            self.stats.game_status = 'user_lose'
        else:
            snake_tail = self.snake.pop()
            draw_message(*snake_tail, self.game_area.box, ' ')

    def handle_snake_eat_food(self):
        self.food = None
        self.put_food_on_field()

        self.stats.score += 1
        self.show_side_menu_tips(
            game_state=self.tips,
            game_tips=GAME_TIPS,
        )
        self.achievement_manager.check(set_pause=True)

    @log
    def save_game_data(self):
        update_total_games_count(self.game_name, 1)
        update_total_time_count(self.game_name, self.start_time)

        if self.stats.score > self.stats.best_score:
            update_best_score(self.game_name, self.stats.score)
