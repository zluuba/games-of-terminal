from games_of_terminal.games.tetris.constants import (
    CELL_HEIGHT, CELL_WIDTH, NEXT_BLOCK_TEXT,
    NEXT_BLOCK_AREA_HEIGHT,
)
from games_of_terminal.constants import DEFAULT_COLOR
from games_of_terminal.sub_window import SubWindow
from games_of_terminal.utils import (
    init_curses_colors, get_color_by_name,
    draw_message,
)


class NextBlockArea:
    def __init__(self, parent_window, game_board):
        init_curses_colors()

        self.height = NEXT_BLOCK_AREA_HEIGHT * CELL_HEIGHT
        self.width = NEXT_BLOCK_AREA_HEIGHT * CELL_WIDTH

        self.next_block_area = SubWindow(
            parent_window.box, self.height, self.width,
            game_board.begin_y + 1, game_board.begin_x + game_board.width + 1,
        )
        self.win = self.next_block_area.box

    def _draw_cell(self, y, x, color_name, size=1):
        color = get_color_by_name(color_name)
        draw_message(y, x, self.win, ' ' * size, color)

    def show(self, block):
        self.clear_window()
        self.show_next_block_title()

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
                self._draw_cell(row, col, DEFAULT_COLOR)

    def show_next_block_title(self):
        begin_y = 0     # top border
        begin_x = (self.width // 2) - (len(NEXT_BLOCK_TEXT) // 2)
        draw_message(begin_y, begin_x, self.win, NEXT_BLOCK_TEXT, DEFAULT_COLOR)
