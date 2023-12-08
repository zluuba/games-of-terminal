from games_of_terminal.games.tetris.constants import (
    BLOCKS, BLOCK_COLORS,
    OFFSETS, CELL_HEIGHT, CELL_WIDTH,
)
from games_of_terminal.colors import Colors
from copy import deepcopy


class TetrisBlock(Colors):
    def __init__(self, name, y, x, board):
        super().__init__()

        self.y = y
        self.x = x
        self.name = name
        self.board = board

        self.color_name = BLOCK_COLORS[name]
        self.color = self.get_color_by_name(self.color_name)

        self.blueprint = deepcopy(BLOCKS[name])

        self.height = len(self.blueprint)
        self.width = len(self.blueprint[0])

    def move(self, direction):
        y_offset, x_offset = OFFSETS[direction]
        y_offset *= CELL_HEIGHT
        x_offset *= CELL_WIDTH

        if self._is_out_of_borders(y_offset=y_offset, x_offset=x_offset):
            return
        if self._is_there_another_blocks(y_offset=y_offset, x_offset=x_offset):
            return

        self.y += y_offset
        self.x += x_offset

    def flip(self):
        new_blueprint = list(zip(*self.blueprint[::-1]))

        if self._is_out_of_borders(blueprint=new_blueprint):
            return

        self.blueprint = new_blueprint
        self.height = len(self.blueprint)
        self.width = len(self.blueprint[0])

    def drop(self):
        y_offset = 0

        while True:
            new_y_offset = y_offset + CELL_HEIGHT

            if self._is_out_of_borders(y_offset=new_y_offset):
                break
            if self._is_there_another_blocks(y_offset=new_y_offset):
                break

            y_offset = new_y_offset

        self.y += y_offset

    def _is_there_another_blocks(self, x_offset=0, y_offset=0):
        begin_y = self.y + y_offset
        begin_x = self.x + x_offset

        end_y = begin_y + (self.height * CELL_HEIGHT)
        end_x = begin_x + (self.width * CELL_WIDTH)

        for y in range(begin_y, end_y, CELL_HEIGHT):
            for x in range(begin_x, end_x, CELL_WIDTH):
                blueprint_y = (y - begin_y) // CELL_HEIGHT
                blueprint_x = (x - begin_x) // CELL_WIDTH
                blueprint_cell = self.blueprint[blueprint_y][blueprint_x]

                if blueprint_cell and not self.board.is_cell_free(y, x):
                    return True
        return False

    def _is_out_of_borders(self, y_offset=0, x_offset=0, blueprint=None):
        if blueprint is None:
            blueprint = self.blueprint

        height = len(blueprint)
        width = len(blueprint[0])

        begin_x = self.x + x_offset
        begin_y = self.y + y_offset

        end_x = begin_x + (width * CELL_WIDTH)
        end_y = begin_y + (height * CELL_HEIGHT)

        if begin_x <= 0:                    # left border
            return True
        if end_x > self.board.width + 1:    # right border
            return True
        if end_y >= self.board.height:      # bottom border
            return True
        return False
