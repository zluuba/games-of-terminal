from games_of_terminal.colors import Colors
from games_of_terminal.field import Field

from games_of_terminal.games.tetris.constants import (
    CELL_HEIGHT, CELL_WIDTH, NEXT_BLOCK_TEXT,
    NEXT_BLOCK_AREA_HEIGHT,
)


class NextBlockArea(Colors):
    def __init__(self, parent_window, game_board):
        super().__init__()

        self.height = NEXT_BLOCK_AREA_HEIGHT * CELL_HEIGHT
        self.width = NEXT_BLOCK_AREA_HEIGHT * CELL_WIDTH

        self.next_block_area = Field(
            parent_window.box, self.height, self.width,
            game_board.begin_y + 1, game_board.begin_x + game_board.width + 1,
            show_borders=True,
        )
        self.win = self.next_block_area.box

    def _draw_cell(self, y, x, color_name, size=1):
        color = self.get_color_by_name(color_name)

        self.win.addstr(y, x, ' ' * size, color)
        self.win.refresh()

    def show(self, block):
        self.clear_window()
        self.draw_text()

        block_y = (self.height // 2) - (block.height * CELL_HEIGHT // 2)
        begin_x = block_x = (self.width // 2) - (block.width * CELL_WIDTH // 2)

        for row in range(block.height):
            for col in range(block.width):
                if block.blueprint[row][col]:
                    self._draw_cell(
                        block_y, block_x, block.color_name, CELL_WIDTH
                    )
                block_x += CELL_WIDTH

            block_y += CELL_HEIGHT
            block_x = begin_x

    def clear_window(self):
        for row in range(1, self.height - 1):
            for col in range(1, self.width - 1):
                self._draw_cell(row, col, self.default_color)

    def draw_text(self):
        begin_y = 0     # top border
        begin_x = (self.width // 2) - (len(NEXT_BLOCK_TEXT) // 2)
        self.win.addstr(begin_y, begin_x, NEXT_BLOCK_TEXT, self.default_color)
        self.win.refresh()
