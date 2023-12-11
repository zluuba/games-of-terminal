from games_of_terminal.colors import Colors
from games_of_terminal.field import Field

from games_of_terminal.games.tetris.constants import (
    CELL_HEIGHT, CELL_WIDTH,
)


class NextBlockArea(Colors):
    def __init__(self, parent_window, game_board):
        super().__init__()

        self.height = 6
        self.width = 6 * 2

        self.next_block_area = Field(
            parent_window.box, self.height, self.width,
            game_board.begin_y + 1, game_board.begin_x + game_board.width + 1,
            show_borders=False,
        )
        self.win = self.next_block_area.box

    def _draw_cell(self, y, x, color_name, size=1):
        color = self.get_color_by_name(color_name)

        self.win.addstr(y, x, ' ' * size, color)
        self.win.refresh()

    def show(self, block):
        self.win.clear()
        self.draw_text()

        block_y = (self.height - block.height) // 2
        begin_x = block_x = (self.width - block.width) // 2

        for row in range(block.height):
            for col in range(block.width):
                if not block.blueprint[row][col]:
                    block_x += CELL_WIDTH
                    continue

                self._draw_cell(block_y, block_x, block.color_name, CELL_WIDTH)
                block_x += CELL_WIDTH

            block_y += CELL_HEIGHT
            block_x = begin_x

    def draw_text(self):
        text = 'next'
        begin_y = 0
        begin_x = (self.width - len(text)) // 2
        self.win.addstr(begin_y, begin_x, text, self.default_color)
        self.win.refresh()
