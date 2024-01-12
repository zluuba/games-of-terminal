from games_of_terminal.constants import BASE_OFFSET
from games_of_terminal.games.tetris.constants import (
    FIELD_WIDTH, CELL_WIDTH, CELL_HEIGHT,
)
from games_of_terminal.sub_window import SubWindow
from games_of_terminal.utils import (
    init_curses_colors, get_color_by_name,
)


class TetrisBoard:
    def __init__(self, parent_window):
        init_curses_colors()

        self.height = parent_window.height
        self.width = FIELD_WIDTH * CELL_WIDTH
        self.begin_y = None
        self.begin_x = None

        self.landed_blocks = dict()
        self.bg_color_name = 'white_text_dark_grey_bg'

        self.board_window = self.create_board_window(parent_window)
        self.win = self.board_window.box

        self.draw_background()

    def create_board_window(self, parent_window):
        window_width = self.width + BASE_OFFSET

        self.begin_y = parent_window.begin_y
        self.begin_x = ((parent_window.begin_x + parent_window.width) // 2) - (window_width // 2)

        return SubWindow(parent_window.box, self.height, window_width,
                         self.begin_y, self.begin_x, show_borders=False)

    def is_cell_free(self, y, x):
        return (y, x) not in self.landed_blocks

    def hide_cell(self, y, x, *args):
        self.draw_cell(y, x, self.bg_color_name, CELL_WIDTH)

    def land_cell(self, y, x, color, *args):
        self.landed_blocks[(y, x)] = color

    def draw_board(self, block=None):
        self.draw_background()
        self.draw_landed_blocks()

        if block:
            self.change_block(block, action='draw')

    def draw_cell(self, y, x, color_name, size=1):
        color = get_color_by_name(color_name)

        self.win.addstr(y, x, ' ' * size, color)
        self.win.refresh()

    def draw_background(self):
        y_start, y_end = 1, self.height - 1
        x_start, x_end = 1, self.width + 1

        for y in range(y_start, y_end):
            for x in range(x_start, x_end):
                self.draw_cell(y, x, self.bg_color_name)

    def change_block(self, block, action='draw'):
        actions = {
            'draw': self.draw_cell,
            'hide': self.hide_cell,
            'land': self.land_cell,
        }

        take_action = actions[action]

        block_y = block.y
        begin_x = block_x = block.x

        for row in range(block.height):
            for col in range(block.width):
                if not block.blueprint[row][col]:
                    block_x += CELL_WIDTH
                    continue

                take_action(block_y, block_x, block.color_name, CELL_WIDTH)
                block_x += CELL_WIDTH

            block_y += CELL_HEIGHT
            block_x = begin_x

    def draw_landed_blocks(self):
        for (y, x), color in self.landed_blocks.items():
            self.draw_cell(y, x, color, CELL_WIDTH)

    def get_complete_line(self, complete_line=0):
        for y in range(self.height - 2, 1, -1):
            occupied_cells = [x for x in range(1, self.width + 1) if (y, x) in self.landed_blocks.keys()]

            if len(occupied_cells) == (self.width // CELL_WIDTH):
                complete_line = y
                break
            if not occupied_cells:
                break

        return complete_line

    def remove_line(self, line_y):
        new_landed_blocks = dict()

        for (ly, lx), color in self.landed_blocks.items():
            if ly < line_y:
                new_landed_blocks[(ly + 1, lx)] = color
            elif ly > line_y:
                new_landed_blocks[(ly, lx)] = color

        self.landed_blocks = new_landed_blocks
