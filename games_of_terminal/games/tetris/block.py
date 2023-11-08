from games_of_terminal.games.tetris.constants import (
    BLOCKS, OFFSETS, CELL_HEIGHT, CELL_WIDTH,
    BLOCK_COLORS,
)
from games_of_terminal.colors import Colors
from copy import deepcopy


class TetrisBlock(Colors):
    def __init__(self, name, game_area):
        super().__init__()

        self.name = name

        color_name = BLOCK_COLORS[name]
        self.color = self.get_color_by_name(color_name)

        self.blueprint = deepcopy(BLOCKS[name])

        self.height = len(self.blueprint)
        self.width = len(self.blueprint[0])

        self.coordinates = None
        self.game_area = game_area

    def draw(self, color=None):
        if color is None:
            color = self.color

        begin_y, begin_x = self.coordinates

        for row in range(0, (self.height * CELL_HEIGHT), CELL_HEIGHT):
            for col in range(0, (self.width * CELL_WIDTH), CELL_WIDTH):
                y = begin_y + row
                x = begin_x + col

                if self.blueprint[row // CELL_HEIGHT][col // CELL_WIDTH]:
                    self.draw_cell(y, x, color)

    def draw_cell(self, y, x, color):
        self.game_area.box.addstr(y, x, '  ', color)
        self.game_area.box.refresh()

    def move(self, direction):
        y_offset, x_offset = OFFSETS[direction]
        y_offset *= CELL_HEIGHT
        x_offset *= CELL_WIDTH

        if self._is_out_of_walls(x_offset):
            return

        # hide current block
        self.draw(self.default_color)

        begin_y, begin_x = self.coordinates

        self.coordinates = (begin_y + y_offset, begin_x + x_offset)
        self.draw()

    def _is_out_of_walls(self, x_offset):
        _, begin_x = self.coordinates
        begin_x += x_offset
        end_x = begin_x + (self.width * CELL_WIDTH)

        if begin_x <= self.game_area.left_border:
            return True
        if end_x >= self.game_area.right_border:
            return True

        return False

    def flip(self):
        # hide current block
        self.draw(self.default_color)

        self.blueprint = list(zip(*self.blueprint[::-1]))
        self.height = len(self.blueprint)
        self.width = len(self.blueprint[0])

        self.draw()
