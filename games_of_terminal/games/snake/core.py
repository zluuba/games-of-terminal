from games_of_terminal.constants import KEYS
from games_of_terminal.database.database import get_game_settings
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

        self.apply_user_settings()

        self.snake = self.get_initial_snake()
        self.food = self.get_food_coords()
        self.direction = KEYS['right_arrow']

        self.obstacles = self.get_obstacles()

        self.start_time = time()
        self.achievement_manager = SnakeGameAchievementsManager(self)

    def apply_user_settings(self):
        settings = get_game_settings(self.game_name)
        self.setup_colors(settings)
        self.setup_skins(settings)
        self.setup_mode(settings)

    def setup_colors(self, settings):
        color_scheme = get_current_color_scheme_name(
            settings['color_schemes']
        )
        snake_color_name = COLORS[color_scheme]['snake']
        food_color_name = COLORS[color_scheme]['food']
        obstacles_color_name = COLORS[color_scheme]['obstacles']

        self.snake_color = get_color_by_name(snake_color_name)
        self.food_color = get_color_by_name(food_color_name)
        self.obstacles_color = get_color_by_name(obstacles_color_name)

    def setup_skins(self, settings):
        self.snake_skin = self.get_selected_option(
            settings['snake_skins'], 'skin',
        )
        self.food_skin = self.get_selected_option(
            settings['food_skins'], 'skin',
        )

    def setup_mode(self, settings):
        self.mode = self.get_selected_option(
            settings['modes'], 'name',
        )

    def get_initial_snake(self):
        middle_y = self.game_area.height // 2
        middle_x = self.game_area.width // 2

        return [[middle_y, middle_x + 1],
                [middle_y, middle_x],
                [middle_y, middle_x - 1]]

    @staticmethod
    def get_selected_option(options, option_type):
        for option in options:
            if option['selected']:
                return option[option_type]

    def get_obstacles(self):
        obstacles = []
        obstacles_count = 10    # temp, should be dynamic

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

            if self.is_user_win():
                self.stats.game_status = 'user_win'
            if self.is_snake_eat_itself() or self.is_snake_touch_the_border():
                self.stats.game_status = 'user_lose'

    def controller(self, key, pause_on=True):
        super().controller(key, pause_on)

        if key in DIRECTIONS.keys():
            self.change_direction(key)

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
        new_snake_head = self.get_new_snake_head()
        obstacles = self.get_all_obstacles_coords()

        if new_snake_head == self.food:
            self.handle_snake_eat_food()
        elif new_snake_head in obstacles:
            self.stats.game_status = 'user_lose'
        else:
            snake_tail_coordinates = self.snake.pop()
            draw_message(*snake_tail_coordinates, self.game_area.box, ' ')

        self.snake.insert(0, new_snake_head)
        draw_message(*new_snake_head, self.game_area.box,
                     self.snake_skin, self.snake_color)

    def get_new_snake_head(self):
        snake_head_y, snake_head_x = self.snake[0]

        if self.direction == KEYS['right_arrow']:
            return [snake_head_y, snake_head_x + 1]
        elif self.direction == KEYS['left_arrow']:
            return [snake_head_y, snake_head_x - 1]
        elif self.direction == KEYS['up_arrow']:
            return [snake_head_y - 1, snake_head_x]
        return [snake_head_y + 1, snake_head_x]

    def handle_snake_eat_food(self):
        self.food = None
        self.put_food_on_field()

        self.stats.score += 1
        self.show_side_menu_tips(
            game_state=self.tips,
            game_tips=GAME_TIPS,
        )
        self.achievement_manager.check(set_pause=True)

    def is_user_win(self):
        """Checks whether every coordinate on the field
        is occupied by a snake, obstacle, or food.
        If true, the user wins.
        """
        top_y = self.game_area.top_border + 1
        bottom_y = self.game_area.bottom_border - 1
        left_x = self.game_area.left_border + 1
        right_x = self.game_area.right_border - 1

        field_len = (right_x + 1 - left_x) * (bottom_y + 1 - top_y)
        occupied_len = len(self.snake) + len(self.obstacles) + 1   # 1 is food

        return field_len == occupied_len

    @log
    def save_game_data(self):
        update_total_time_count(self.game_name, self.start_time)

        if self.is_game_over():
            update_total_games_count(self.game_name, 1)

        if self.stats.score > self.stats.best_score:
            update_best_score(self.game_name, self.stats.score)

    def draw_game_window(self):
        self.window.erase()

        self.draw_basic_window_view()
        self.show_side_menu_tips(
            game_state=self.tips,
            game_tips=GAME_TIPS,
        )

        self.apply_user_settings()
        self.put_snake_on_field()
        self.put_food_on_field()
        self.put_obstacles_on_field()

        self.check_achievements()

    def check_achievements(self):
        if self.is_settings_option_was_change('snake_skins'):
            self.achievement_manager.check(snake_color_scheme_change=True)
        if self.is_settings_option_was_change('modes'):
            self.achievement_manager.check(game_mode_change=True)
