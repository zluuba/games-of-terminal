from games_of_terminal.database.database import get_game_state, save_game_state
from games_of_terminal.games.engine import GameEngine
from games_of_terminal.games.tetris.block import TetrisBlock
from games_of_terminal.games.tetris.game_board import TetrisBoard
from games_of_terminal.games.tetris.next_block import NextBlockArea
from games_of_terminal.games.tetris.constants import (
    BLOCKS, DIRECTIONS, FLIP_BLOCK, DROP_BLOCK,
    CELL_WIDTH, CELL_HEIGHT, DOWN, SCORES, LEVELS,
)

from time import time
from random import choice


class TetrisGame(GameEngine):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.block = None
        self.next_block = None
        self.board = None
        self.falling_direction = 'down'

        self.score = 0
        self.best_score = None
        self.level = 1
        self.time_interval = 1
        self.time = time()

    @property
    def tips(self):
        return {
            'Score': self.score,
            'Level': self.level,
            'Best Score': self.best_score,
        }

    def set_best_score(self):
        data = get_game_state('Tetris', 'best_score')
        self.best_score = data

    def save_best_score(self):
        if self.score > self.best_score:
            save_game_state('Tetris', 'best_score', self.score)

    def start_new_game(self):
        self._game_setup()

        while True:
            self.create_block()
            key = self.window.getch()
            self.controller(key)

            if self.is_exit:
                return
            if self.is_game_over():
                self.save_best_score()
                is_restart = self.ask_for_restart()
                if not is_restart:
                    return

            self._block_auto_move()

            if self.is_block_on_floor():
                self.move_block_before_land()
                self.land_current_block()

    def controller(self, key, pause_off=False):
        super().controller(key, pause_off)

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

        self.board.block(self.block, 'land')
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

        self.score += SCORES[lines_count] * self.level
        self._increase_level()
        self.draw_game_tips(self.tips)
        self.board.draw_board()

    def _increase_level(self):
        if self.level == max(LEVELS):
            return

        min_score_to_up_level = LEVELS[self.level + 1]
        if self.score >= min_score_to_up_level:
            self.level += 1
            self.time_interval -= 0.2

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

    def _game_setup(self):
        self.hide_cursor()
        self.window.nodelay(1)

        self.set_best_score()

        self.setup_side_menu()
        self.show_game_status()
        self.draw_game_tips(self.tips)

        self.time = time()
        self.board = TetrisBoard(self.game_area)
        self.next_block_area = NextBlockArea(self.game_area, self.board)

    def create_block(self):
        if self.block:
            return
        if self.next_block:
            self.block = self.next_block
            self.next_block = self.get_new_block()
        if not self.block:
            self.block = self.get_new_block()
        if not self.next_block:
            self.next_block = self.get_new_block()

        self.board.draw_board(self.block)
        self.next_block_area.show(self.next_block)

        # check new block for correct placement
        if self.block.is_block_placed_in_land():
            self.game_status = 'user_lose'

    def get_new_block(self):
        block_shape_name = choice(list(BLOCKS))
        y, x = 1, self.board.width // 2

        block = TetrisBlock(block_shape_name, y, x, self.board)

        # these lines place block in the center of board
        block.x -= (block.width * CELL_WIDTH) // 2
        block.x += 1 if block.x % 2 == 0 else 0

        return block

    def _block_auto_move(self):
        current_time = time()

        if current_time - self.time >= self.time_interval:
            self.block.move(self.falling_direction)
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
