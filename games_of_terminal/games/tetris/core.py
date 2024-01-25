from games_of_terminal.database.database import (
    get_game_stat_value, update_game_stat,
)
from games_of_terminal.games.engine import GameEngine
from games_of_terminal.games.tetris.block import TetrisBlock
from games_of_terminal.games.tetris.game_board import TetrisBoard
from games_of_terminal.games.tetris.next_block import NextBlockArea
from games_of_terminal.games.tetris.constants import (
    CELL_WIDTH, CELL_HEIGHT, BLOCKS,
    DIRECTIONS, FLIP_BLOCK, DROP_BLOCK,
    DOWN, SCORES, LEVELS, GAME_TIPS,
    LEVEL_SPEED_DIFF, FALLING_DIRECTION,
)
from games_of_terminal.log import log
from games_of_terminal.utils import (
    hide_cursor,
    update_total_time_count,
    update_total_games_count,
    update_best_score,
)

from time import time
from random import choice


class TetrisGame(GameEngine):
    def __repr__(self):
        return '<TetrisGame>'

    @log
    def setup_game_stats(self):
        self.block = None
        self.next_block = None
        self.board = None

        self.level = 1
        self.time_interval = 1
        self.start_time = self.time = time()

        self.lines_removed = 0

    @log
    def setup_game_field(self):
        hide_cursor()
        self.window.nodelay(1)
        self.window.timeout(150)

        self.set_best_score()

        self.draw_logo()
        self.show_side_menu_tips(
            game_state=self.tips,
            game_tips=GAME_TIPS,
        )
        self.show_game_status()

        self.board = TetrisBoard(self.game_area)
        self.next_block_area = NextBlockArea(self.game_area, self.board)

        self.time = time()

    @log
    def start_new_game(self):
        self.create_block()

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

            self.block_auto_move()

            if self.is_block_on_floor():
                self.move_block_before_land()
                self.land_current_block()
            if not self.block:
                self.create_block()

    @property
    def tips(self):
        return {
            'Level': self.level,
            'Score': self.stats.score,
            'Best Score': self.stats.best_score,
            'Lines Removed': self.lines_removed,
        }

    @log
    def set_best_score(self):
        data = get_game_stat_value(self.game_name, 'best_score')
        self.stats.best_score = int(data)

    def controller(self, key, pause_on=True):
        super().controller(key, pause_on)

        if key == FLIP_BLOCK:
            self.block.flip()
        elif key == DROP_BLOCK:
            self.block.drop()
            self.land_current_block()
        elif key in DIRECTIONS:
            direction = DIRECTIONS[key]
            self.block.move(direction)

    def land_current_block(self):
        if not self.is_block_on_floor():
            return

        self.board.change_block(self.block, 'land')
        self.block = None
        self.time = time()
        self.board.draw_board()

        self.remove_complete_lines()
        self.create_block()

    def remove_complete_lines(self):
        lines_count = 0

        while True:
            line_y = self.board.get_complete_line()
            if not line_y:
                break

            lines_count += 1
            self.board.remove_line(line_y)

        if not lines_count:
            return

        self.lines_removed += lines_count
        self.stats.score += SCORES[lines_count] * self.level
        self.increase_level()
        self.show_side_menu_tips(
            game_state=self.tips,
            game_tips=GAME_TIPS,
        )
        self.board.draw_board()

    @log
    def increase_level(self):
        if self.level == max(LEVELS):
            return

        min_score_to_up_level = LEVELS[self.level + 1]
        if self.stats.score >= min_score_to_up_level:
            self.level += 1
            self.time_interval -= LEVEL_SPEED_DIFF

    def move_block_before_land(self):
        """ Give the ability move block if it touches the floor """

        current_time = time()

        while current_time - self.time < self.time_interval:
            key = self.window.getch()

            if key == FLIP_BLOCK:
                self.block.flip()
            elif key == DOWN:
                break
            elif key in DIRECTIONS:
                direction = DIRECTIONS[key]
                self.block.move(direction)
                self.board.draw_board(self.block)

                if not self.is_block_on_floor():
                    return

            current_time = time()
        self.time = current_time

    def create_block(self):
        if self.block:
            return
        if self.next_block:
            self.block = self.next_block
            self.next_block = None
        if not self.block:
            self.block = self.get_new_block()
        if not self.next_block:
            self.next_block = self.get_new_block()

        self.board.draw_board(self.block)
        self.next_block_area.show(self.next_block)

        # check new block for correct placement
        if self.block.is_block_placed_in_land():
            self.stats.game_status = 'user_lose'

    def get_new_block(self):
        block_shape_name = choice(list(BLOCKS))
        y, x = 1, self.board.width // 2

        block = TetrisBlock(block_shape_name, y, x, self.board)

        # these lines place block in the center of board
        block.x -= (block.width * CELL_WIDTH) // 2
        block.x += 1 if block.x % 2 == 0 else 0

        return block

    def block_auto_move(self):
        current_time = time()

        if current_time - self.time >= self.time_interval:
            self.block.move(FALLING_DIRECTION)
            self.board.draw_board(self.block)
            self.time = current_time

    def is_block_on_floor(self):
        begin_y = self.block.y
        begin_x = self.block.x

        end_y = begin_y + (self.block.height * CELL_HEIGHT)
        end_x = begin_x + (self.block.width * CELL_WIDTH)

        for y in range(begin_y, end_y, CELL_HEIGHT):
            for x in range(begin_x, end_x, CELL_WIDTH):
                blueprint_y = (y - begin_y) // CELL_HEIGHT
                blueprint_x = (x - begin_x) // CELL_WIDTH
                blueprint_cell = self.block.blueprint[blueprint_y][blueprint_x]

                if blueprint_cell:
                    if not self.board.is_cell_free(y + 1, x):
                        return True
                    if y + 1 >= self.board.board_window.bottom_border:
                        return True
        return False

    @log
    def save_game_data(self):
        update_total_games_count(self.game_name, 1)
        update_total_time_count(self.game_name, self.start_time)

        if self.stats.score > self.stats.best_score:
            update_best_score(self.game_name, self.stats.score)

        self.update_lines_removed_count()

    def update_lines_removed_count(self):
        stat_name = 'lines_removed'

        if self.lines_removed:
            update_game_stat(self.game_name, stat_name, self.lines_removed)
