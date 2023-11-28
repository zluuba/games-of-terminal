from games_of_terminal.games.tetris.constants import (
    BLOCKS, OFFSETS, CELL_HEIGHT, CELL_WIDTH,
    BLOCK_COLORS,
)
from games_of_terminal.colors import Colors
from copy import deepcopy


class TetrisBlock(Colors):
    def __init__(self, name, y, x, board, game_area):
        super().__init__()

        self.y = y
        self.x = x
        self.name = name
        self.board = board
        self.game_area = game_area

        color_name = BLOCK_COLORS[name]
        self.color = self.get_color_by_name(color_name)

        self.blueprint = deepcopy(BLOCKS[name])

        self.height = len(self.blueprint)
        self.width = len(self.blueprint[0])

    def draw(self, color):
        for row in range(0, (self.height * CELL_HEIGHT), CELL_HEIGHT):
            for col in range(0, (self.width * CELL_WIDTH), CELL_WIDTH):
                y = self.y + row
                x = self.x + col

                if self.blueprint[row // CELL_HEIGHT][col // CELL_WIDTH]:
                    self.draw_cell(y, x, color)

    def draw_cell(self, y, x, color):
        self.game_area.box.addstr(y, x, ' ' * CELL_WIDTH, color)
        self.game_area.box.refresh()

    def hide(self):
        background_color = self.default_color
        self.draw(background_color)

    def move(self, direction):
        y_offset, x_offset = OFFSETS[direction]
        y_offset *= CELL_HEIGHT
        x_offset *= CELL_WIDTH

        if self._is_out_of_borders(x_offset=x_offset):
            return
        if self._is_there_another_blocks(x_offset=x_offset):
            return

        self.hide()

        self.y += y_offset
        self.x += x_offset
        self.draw(self.color)

    def flip(self):
        new_blueprint = list(zip(*self.blueprint[::-1]))

        if self._is_out_of_borders(blueprint=new_blueprint):
            return

        self.hide()

        self.blueprint = new_blueprint
        self.height = len(self.blueprint)
        self.width = len(self.blueprint[0])

        self.draw(self.color)

    def drop(self):
        y_offset = 0 * CELL_HEIGHT

        while True:
            new_y_offset = y_offset + (1 * CELL_HEIGHT)

            if self._is_out_of_borders(y_offset=new_y_offset - 1):
                break
            if self._is_there_another_blocks(y_offset=new_y_offset):
                break

            y_offset = new_y_offset

        self.hide()
        self.y += y_offset
        self.draw(self.color)

    def land(self):
        end_y = self.y + (self.height * CELL_HEIGHT)
        end_x = self.x + (self.width * CELL_WIDTH)

        for y in range(self.y, end_y, CELL_HEIGHT):
            for x in range(self.x, end_x, CELL_WIDTH):
                for x_offset in range(CELL_WIDTH):
                    new_x = x + x_offset

                    blueprint_y = (y - self.y) // CELL_HEIGHT
                    blueprint_x = (new_x - self.x) // CELL_WIDTH
                    blueprint_cell = self.blueprint[blueprint_y][blueprint_x]

                    if blueprint_cell:
                        self.board.place_block(y, new_x)

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

        width = len(blueprint[0])
        height = len(blueprint)

        end_x = self.x + x_offset + (width * CELL_WIDTH)
        end_y = self.y + y_offset + (height * CELL_HEIGHT)

        if self.x + x_offset <= self.game_area.left_border:
            return True
        if end_x >= self.game_area.right_border:
            return True
        if end_y >= self.game_area.bottom_border:
            return True

        return False
