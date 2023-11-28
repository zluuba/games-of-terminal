from games_of_terminal.constants import KEYS, DEFAULT_OFFSET
from games_of_terminal.games.engine import GameEngine
from games_of_terminal.games.tetris.block import TetrisBlock
from games_of_terminal.games.tetris.game_board import TetrisBoard

from games_of_terminal.games.tetris.constants import (
    BLOCKS, DIRECTIONS, FLIP_BLOCK, DROP_BLOCK,
    CELL_WIDTH, CELL_HEIGHT, DOWN,
)

from curses import endwin
from time import time
from random import choice


class TetrisGame(GameEngine):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.block = None
        self.board = None
        self.falling_direction = 'down'

        self.score = 0
        self.time_interval = 1
        self.time = time()

    def start_new_game(self):
        self._game_setup()
        self.add_block_on_field()

        self.time = time()

        while True:
            key = self.window.getch()

            if key == KEYS['escape']:
                endwin()
                return

            if key == FLIP_BLOCK:
                self.block.flip()
            elif key == DROP_BLOCK:
                self.block.drop()
                self.land_current_block()
                self.add_block_on_field()
                continue
            elif key in DIRECTIONS:
                direction = DIRECTIONS[key]
                self.block.move(direction)

            self._block_auto_move()

            if self.is_block_on_floor():
                self.land_current_block(last_move=True)
                self.add_block_on_field()

    def land_current_block(self, last_move=False):
        """ Give the ability move block if it touches the floor """

        if last_move:
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

                current_time = time()
            self.time = current_time

        self.block.land()
        self.board.draw()

    def _game_setup(self):
        self.hide_cursor()
        self.window.nodelay(1)

        self.setup_side_menu()
        self.show_game_status()

        self._setup_game_window()

    def _setup_game_window(self):
        self.board = TetrisBoard(self.game_area)

        # TODO: add next_block_area

    def add_block_on_field(self):
        block_shape_name = choice(list(BLOCKS))

        y = self.game_area.begin_y
        x = (self.game_area.width - DEFAULT_OFFSET) // 2

        self.block = TetrisBlock(block_shape_name, y, x, self.board, self.game_area)
        self.block.draw(self.block.color)

    def _block_auto_move(self):
        current_time = time()

        if current_time - self.time >= self.time_interval:
            self.block.move(self.falling_direction)
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
                    if (y + 1, x) in self.board.board and not self.board.is_cell_free(y + 1, x):
                        return True
                    if y + 1 >= self.game_area.bottom_border:
                        return True
        return False
