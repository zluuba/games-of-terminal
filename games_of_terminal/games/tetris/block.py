from games_of_terminal.games.tetris.constants import (
    BLOCKS, OFFSETS, CELL_HEIGHT, CELL_WIDTH,
)


class TetrisBlock:
    def __init__(self, name):
        self.name = name
        self.blueprint = BLOCKS[name]

        self.height = len(self.blueprint)
        self.width = len(self.blueprint[0])

        self.cells = []
        self.coordinates = None

    def add_cell(self, r, c, cell, owner='free'):
        self.blueprint[r][c] = cell
        cell.owner = owner

    def show(self):
        for row in range(self.height):
            for col in range(self.width):
                cell = self.blueprint[row][col]
                cell.colorize()

    def hide_cell(self, cell):
        cell.set_free()
        cell.colorize()

    def move(self, direction, field_cells):
        y_offset, x_offset = OFFSETS[direction]

        if self._is_out_of_bounds(y_offset, x_offset, field_cells):
            return

        for row in range(self.height):
            for col in range(self.width):
                cell = self.blueprint[row][col]

                y, x = cell.coordinates
                new_y = y + (y_offset * CELL_HEIGHT)
                new_x = x + (x_offset * CELL_WIDTH)

                new_cell = field_cells[(new_y, new_x)]
                self.blueprint[row][col] = new_cell

                if not cell.is_free():
                    new_cell.owner = self.name
                    cell.set_free()
                    cell.colorize()

        self.show()

    def _is_out_of_bounds(self, y_offset, x_offset, field_cells):
        for row in range(self.height):
            for col in range(self.width):
                cell = self.blueprint[row][col]

                y, x = cell.coordinates
                new_y = y + (y_offset * CELL_HEIGHT)
                new_x = x + (x_offset * CELL_WIDTH)

                if (new_y, new_x) not in field_cells:
                    return True
        return False

    def flip(self):
        # self.blueprint = list(zip(*self.blueprint[::-1]))
        pass
