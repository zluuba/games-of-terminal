from games_of_terminal.games.tetris.constants import (
    FIELD_WIDTH, CELL_WIDTH, CELL_HEIGHT, BASE_OFFSET,
)
from games_of_terminal.colors import Colors
from games_of_terminal.field import Field


class TetrisBoard(Colors):
    def __init__(self, parent_window):
        super().__init__()

        self.height = parent_window.height
        self.width = FIELD_WIDTH * CELL_WIDTH

        self.bg_color_name = 'white_text_dark_grey_bg'

        self.board_window = self._create_board_window(parent_window)
        self.win = self.board_window.box

        self.draw_background()

        # landed blocks storage
        self.landed_blocks = dict()

    def is_cell_free(self, y, x):
        return (y, x) not in self.landed_blocks

    def _create_board_window(self, parent_window):
        window_width = self.width + BASE_OFFSET

        begin_y = parent_window.begin_y
        begin_x = ((parent_window.begin_x + parent_window.width) // 2) - (window_width // 2)

        return Field(parent_window.box, self.height, window_width,
                     begin_y, begin_x, show_borders=False)

    def land_block(self, block):
        block_y = block.y
        begin_x = block_x = block.x

        for row in range(block.height):
            for col in range(block.width):
                if not block.blueprint[row][col]:
                    block_x += CELL_WIDTH
                    continue

                self.landed_blocks[(block_y, block_x)] = block.color_name
                block_x += CELL_WIDTH

            block_y += CELL_HEIGHT
            block_x = begin_x

    def draw_board(self, block):
        self.draw_background()
        self.draw_landed_blocks()

        if block:
            self.draw_block(block)

    def _draw_cell(self, y, x, color_name, size=1):
        color = self.get_color_by_name(color_name)

        self.win.addstr(y, x, ' ' * size, color)
        self.win.refresh()

    def draw_background(self):
        y_start, y_end = 1, self.height - 1
        x_start, x_end = 1, self.width + 1

        for y in range(y_start, y_end):
            for x in range(x_start, x_end):
                self._draw_cell(y, x, self.bg_color_name)

    def draw_block(self, block):
        block_y = block.y
        begin_x = block_x = block.x

        for row in range(block.height):
            for col in range(block.width):
                if not block.blueprint[row][col]:
                    block_x += CELL_WIDTH
                    continue

                self._draw_cell(block_y, block_x, block.color_name, 2)
                block_x += CELL_WIDTH

            block_y += CELL_HEIGHT
            block_x = begin_x

    def draw_landed_blocks(self):
        for (y, x), color in self.landed_blocks.items():
            self._draw_cell(y, x, color, 2)
