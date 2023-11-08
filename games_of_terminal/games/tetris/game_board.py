from games_of_terminal.games.tetris.constants import (
    CELL_WIDTH, CELL_HEIGHT, BLOCK_COLORS,
)
from games_of_terminal.colors import Colors


class TetrisBoard(Colors):
    def __init__(self, game_box):
        super().__init__()

        self.game_box = game_box
        self.box = {}

        self.setup_board()

    def setup_board(self):
        for y in range(self.game_box.begin_y, self.game_box.height - self.game_box.begin_y):
            for x in range(self.game_box.begin_x, self.game_box.width - self.game_box.begin_x):
                self.box[(y, x)] = 'free'

    def land_block(self, block):
        begin_y, begin_x = block.coordinates

        end_y = begin_y + (block.height * CELL_HEIGHT)
        end_x = begin_x + (block.width * CELL_WIDTH)

        for y in range(begin_y, end_y, CELL_HEIGHT):
            for x in range(begin_x, end_x, CELL_WIDTH):
                for x_offset in range(CELL_WIDTH):
                    new_x = x + x_offset

                    blueprint_y = (y - begin_y) // CELL_HEIGHT
                    blueprint_x = (new_x - begin_x) // CELL_WIDTH
                    blueprint_cell = block.blueprint[blueprint_y][blueprint_x]

                    if blueprint_cell:
                        self.box[(y, new_x)] = 'placed_block'

    def draw(self):
        for coords, val in self.box.items():
            y, x = coords

            color_name = BLOCK_COLORS[val]
            color = self.get_color_by_name(color_name)

            self.game_box.box.addstr(y, x, ' ', color)
            self.game_box.box.refresh()