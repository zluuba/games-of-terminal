from games_of_terminal.games.tetris.constants import (
    CELL_WIDTH, CELL_HEIGHT, BLOCK_COLORS,
)
from games_of_terminal.colors import Colors


class TetrisBoard(Colors):
    def __init__(self, game_box):
        super().__init__()

        self.game_box = game_box
        self.board = {}

        self.setup_board()

    def setup_board(self):
        for y in range(self.game_box.begin_y, self.game_box.height - self.game_box.begin_y):
            for x in range(self.game_box.begin_x + 1, self.game_box.width - self.game_box.begin_x - 1):
                self.board[(y, x)] = 'free'

    def is_cell_free(self, y, x):
        return self.board[(y, x)] == 'free'

    def place_block(self, y, x):
        self.board[(y, x)] = 'placed_block'

    def draw(self):
        for coords, block_type in self.board.items():
            y, x = coords

            color_name = BLOCK_COLORS[block_type]
            color = self.get_color_by_name(color_name)

            self.game_box.box.addstr(y, x, ' ', color)
            self.game_box.box.refresh()
