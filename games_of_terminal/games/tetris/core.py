from games_of_terminal.constants import KEYS
from games_of_terminal.games.engine import GameEngine
from games_of_terminal.games.tetris.cell import TetrisCell
from games_of_terminal.games.tetris.block import TetrisBlock

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

        self.score = 0
        self.cells = {}

        self.block = None
        self.falling_direction = 'down'

        self.time_interval = 1
        self.time = time()

    def _setup_game_field(self):
        self.hide_cursor()
        self.window.nodelay(1)

        self._draw_game_field()
        self._setup_side_menu()
        self.show_game_status()

    def _add_new_block_on_field(self):
        block_shape_name = choice(list(BLOCKS))
        self.block = TetrisBlock(block_shape_name)

        y = self.game_area.begin_y + 1
        x = begin_x = (self.game_area.width - 2) // 2 - self.block.width // 2

        self.block.coordinates = (y, x)

        for i in range(self.block.height):
            for j in range(self.block.width):
                cell = self.cells[(y, x)]

                if self.block.blueprint[i][j]:
                    self.block.add_cell(i, j, cell, self.block.name)
                else:
                    self.block.add_cell(i, j, cell)

                x += CELL_WIDTH

            y += CELL_HEIGHT
            x = begin_x

        self.block.show()

    def start_new_game(self):
        self._setup_game_field()
        self._add_new_block_on_field()

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
                self.block.move(direction, self.cells)

            self._block_auto_move()

    def _block_auto_move(self):
        current_time = time()

        if current_time - self.time >= self.time_interval:
            self.block.move(self.falling_direction, self.cells)
            self.time = current_time

    def _draw_game_field(self):
        lines = (self.game_area.height - 2)
        cols = (self.game_area.width - 2)

        y = self.game_area.begin_y + 1
        x = begin_x = self.game_area.begin_x + 1

        for _ in range(lines):
            for _ in range(cols):
                cell = self._create_cell(y, x)
                self.cells[(y, x)] = cell

                x += 1

            y += 1
            x = begin_x

    def _create_cell(self, y, x):
        field_box = self.game_area.box.subwin(CELL_HEIGHT, CELL_WIDTH, y, x)
        cell = TetrisCell(field_box, (y, x))
        return cell
