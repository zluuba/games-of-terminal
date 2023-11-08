from games_of_terminal.constants import KEYS
from games_of_terminal.games.engine import GameEngine
from games_of_terminal.games.tetris.block import TetrisBlock
from games_of_terminal.games.tetris.game_board import TetrisBoard

from games_of_terminal.games.tetris.constants import (
    BLOCKS, DIRECTIONS, FLIP_BLOCK,
    CELL_WIDTH, CELL_HEIGHT,
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
        self._setup_game_field()
        self.add_new_block_on_field()

        self.time = time()

        while True:
            key = self.window.getch()

            if key == KEYS['escape']:
                endwin()
                return

            if key == FLIP_BLOCK:
                self.block.flip()
            elif key in DIRECTIONS:
                direction = DIRECTIONS[key]
                self.block.move(direction)

            self._block_auto_move()

            if self.is_block_on_floor():
                self.board.land_block(self.block)
                self.board.draw()
                self.add_new_block_on_field()

    def _setup_game_field(self):
        self.hide_cursor()
        self.window.nodelay(1)

        self._setup_side_menu()
        self.show_game_status()

        self.board = TetrisBoard(self.game_area)

    def add_new_block_on_field(self):
        block_shape_name = choice(list(BLOCKS))
        self.block = TetrisBlock(block_shape_name, self.game_area)

        y = self.game_area.begin_y + 1
        x = (self.game_area.width - 2) // 2 - self.block.width // 2

        self.block.coordinates = (y, x)
        self.block.draw()

    def _block_auto_move(self):
        current_time = time()

        if current_time - self.time >= self.time_interval:
            self.block.move(self.falling_direction)
            self.time = current_time

    def is_block_on_floor(self):
        begin_y, begin_x = self.block.coordinates

        end_y = begin_y + (self.block.height * CELL_HEIGHT)
        end_x = begin_x + (self.block.width * CELL_WIDTH)

        for y in range(begin_y, end_y, CELL_HEIGHT):
            for x in range(begin_x, end_x, CELL_WIDTH):
                blueprint_y = (y - begin_y) // CELL_HEIGHT
                blueprint_x = (x - begin_x) // CELL_WIDTH
                blueprint_cell = self.block.blueprint[blueprint_y][blueprint_x]

                if blueprint_cell:
                    end_y = y + CELL_HEIGHT
                    end_x = x + CELL_WIDTH
                    if (end_y, end_x) in self.board.box and self.board.box[(end_y, end_x)] == 'placed_block':
                        return True
                    if end_y >= self.game_area.bottom_border:
                        return True
        return False
