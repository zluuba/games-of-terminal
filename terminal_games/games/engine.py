import curses


LOGO = [
    '######  #####  #####   ##   ##',
    '  ##    ##     ##  ##  ### ###',
    '  ##    ####   ####    ## # ##',
    '  ##    ##     ## ##   ##   ##',
    '  ##    #####  ##  ##  ##   ##',
]


class GameEngine:
    def __init__(self, canvas):
        self.canvas = canvas
        self._setup()

    @staticmethod
    def _init_colors():
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)     # black
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)     # green
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)       # red
        curses.init_pair(4, 1, 236)                                     # dark grey
        curses.init_pair(5, 1, 245)                                     # light grey
        curses.init_pair(6, 1, 132)                                     # pink
        curses.init_pair(7, 1, 134)                                     # light purple

    def _setup(self):
        self.height, self.width = self.canvas.getmaxyx()
        self.canvas.bkgd(' ', curses.color_pair(1))

        self._init_colors()
        self._setup_sizes()

        self._draw_window()
        self._setup_boxes()
        self._draw_logo()

    def _setup_boxes(self):
        self.game_box = self._draw_box(self.sizes['game_box'])
        self.side_menu_box = self._draw_box(self.sizes['side_menu_box'])
        self.logo_box = self._draw_box(self.sizes['logo_box'])

    def _draw_box(self, sizes):
        box = self.window.subwin(*sizes.values())
        box.border()
        return box

    def _draw_window(self):
        sizes = self.sizes['window_box'].values()
        self.window = curses.newwin(*sizes)
        self.window.nodelay(True)
        self.window.keypad(True)

    def _draw_logo(self):
        y, x = 1, 2

        for line in LOGO:
            self.logo_box.addstr(y, x, line)
            y += 1

        self.logo_box.addstr(6, 14, ' GAMES ')

    def _wait(self):
        self.window.timeout(-1)

    def _setup_sizes(self):
        self.sizes = {
            'game_box': {
                'lines': self.height - 2,
                'cols': self.width - 34,
                'begin_y': 1,
                'begin_x': 0,
            },
            'side_menu_box': {
                'lines': self.height - 8,
                'cols': 34,
                'begin_y': 7,
                'begin_x': self.width - 34,
            },
            'logo_box': {
                'lines': 7,
                'cols': 34,
                'begin_y': 1,
                'begin_x': self.width - 34,
            },
            'window_box': {
                'lines': self.height,
                'cols': self.width,
                'begin_y': 0,
                'begin_x': 0,
            },
        }
