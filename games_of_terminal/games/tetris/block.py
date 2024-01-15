from games_of_terminal.games.tetris.constants import (
    BLOCKS, BLOCK_COLORS, CELL_HEIGHT, CELL_WIDTH, OFFSETS,
)
from games_of_terminal.utils import get_color_by_name
from copy import deepcopy


class TetrisBlock:
    def __init__(self, name, y, x, board):
        self.y = y
        self.x = x
        self.name = name
        self.board = board

        self.color_name = BLOCK_COLORS[name]
        self.color = get_color_by_name(self.color_name)

        self.blueprint = deepcopy(BLOCKS[name])

        self.height = len(self.blueprint)
        self.width = len(self.blueprint[0])

    def __repr__(self):
        return f'<TetrisBlock: {self.name}>'

    def move(self, direction):
        y_offset, x_offset = OFFSETS[direction]
        y_offset *= CELL_HEIGHT
        x_offset *= CELL_WIDTH

        if self.is_out_of_borders(y_offset=y_offset, x_offset=x_offset):
            return
        if self.is_there_another_blocks(y_offset=y_offset, x_offset=x_offset):
            return

        self.board.change_block(self, action='hide')
        self.y += y_offset
        self.x += x_offset
        self.board.change_block(self, action='draw')

    def flip(self):
        new_blueprint = list(zip(*self.blueprint[::-1]))

        if self.is_out_of_borders(blueprint=new_blueprint):
            return
        if self.is_there_another_blocks(blueprint=new_blueprint):
            return

        self.board.change_block(self, action='hide')
        self.blueprint = new_blueprint
        self.height = len(self.blueprint)
        self.width = len(self.blueprint[0])
        self.board.change_block(self, action='draw')

    def drop(self):
        # TODO: ineffective, rebuild it

        y_offset = 0

        while True:
            new_y_offset = y_offset + CELL_HEIGHT

            if self.is_out_of_borders(y_offset=new_y_offset):
                break
            if self.is_there_another_blocks(y_offset=new_y_offset):
                break

            y_offset = new_y_offset

        self.board.change_block(self, action='hide')
        self.y += y_offset
        self.board.change_block(self, action='draw')

    def is_there_another_blocks(self, x_offset=0, y_offset=0, blueprint=None):
        if not blueprint:
            blueprint = self.blueprint

        height = len(blueprint)
        width = len(blueprint[0])

        begin_y = self.y + y_offset
        begin_x = self.x + x_offset

        end_y = begin_y + (height * CELL_HEIGHT)
        end_x = begin_x + (width * CELL_WIDTH)

        for y in range(begin_y, end_y, CELL_HEIGHT):
            for x in range(begin_x, end_x, CELL_WIDTH):
                blueprint_y = (y - begin_y) // CELL_HEIGHT
                blueprint_x = (x - begin_x) // CELL_WIDTH
                blueprint_cell = blueprint[blueprint_y][blueprint_x]

                if blueprint_cell and not self.board.is_cell_free(y, x):
                    return True
        return False

    def is_out_of_borders(self, y_offset=0, x_offset=0, blueprint=None):
        if blueprint is None:
            blueprint = self.blueprint

        height = len(blueprint)
        width = len(blueprint[0])

        begin_x = self.x + x_offset
        begin_y = self.y + y_offset

        end_x = begin_x + (width * CELL_WIDTH)
        end_y = begin_y + (height * CELL_HEIGHT)

        if begin_x <= 0:
            return True
        if end_x > self.board.width + 1:
            return True
        if end_y >= self.board.height:
            return True
        return False

    def is_block_placed_in_land(self):
        return self.is_there_another_blocks()
