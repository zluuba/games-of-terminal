from games_of_terminal.constants import KEYS, MESSAGES
from games_of_terminal.games.engine import GameEngine
from games_of_terminal.games.tetris.cell import TetrisCell

from games_of_terminal.games.tetris.constants import (
    BLOCKS, DIRECTIONS, FLIP_BLOCK, DOWN,
    CELL_WIDTH, CELL_HEIGHT,
)

from curses import endwin, flash
from random import choice


class TetrisGame(GameEngine):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.score = 0
        self.cells = {}

        self.block = []
        self.block_coordinates = None

    def _setup_game_field(self):
        self.hide_cursor()
        self.window.nodelay(1)
        self.window.timeout(150)

        self._draw_game_field()
        self._setup_side_menu()
        self.show_game_status()

    def _place_new_block(self):
        shape_color = self.get_random_colored_background_color()

        block_shape_name = choice(list(BLOCKS))
        block_shape = BLOCKS[block_shape_name]

        block_height = len(block_shape)
        block_width = len(block_shape[0])

        y = self.game_area.begin_y + 1
        x = begin_x = (self.game_area.width - 2) // 2 - block_width // 2

        self.block_coordinates = (y, x)

        for i in range(block_height):
            for j in range(block_width):
                cell = self.cells[(y, x)]
                x += CELL_WIDTH

                if not block_shape[i][j]:
                    continue

                cell.owner = 'falling_block'
                cell.block_color = shape_color

            y += CELL_HEIGHT
            x = begin_x

    def start_new_game(self):
        self._setup_game_field()
        self._place_new_block()

        while True:
            key = self.window.getch()
            self.wait_for_keypress()

            if key == KEYS['escape']:
                endwin()
                return

            if key == FLIP_BLOCK:
                self._flip_block(key)
            elif key in DIRECTIONS:
                self._move_block(key)

            # self._move_block('down')

    def _move_block(self, direction):
        if direction == 'down':
            y, x = self.block_coordinates
            self._clear_line(y, x, self.game_area.box, 4)

            self.block_coordinates = y + 1, x

    def _flip_block(self, direction):
        pass

    def _draw_game_field(self):
        lines = (self.game_area.height - 2)
        cols = (self.game_area.width - 2)

        y = self.game_area.begin_y + 1
        x = begin_x = self.game_area.begin_x + 1

        for _ in range(lines):
            for _ in range(cols):
                cell = self._create_cell(y, x)
                self.cells[(y, x)] = cell

                x += 1

            y += 1
            x = begin_x

    def _create_cell(self, y, x):
        field_box = self.game_area.box.subwin(CELL_HEIGHT, CELL_WIDTH, y, x)
        cell = TetrisCell(field_box, (y, x))
        cell.set_background_color()
        return cell
