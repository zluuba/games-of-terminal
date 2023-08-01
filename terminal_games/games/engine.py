import curses


"""
SIZES:

logo:
    width: 31  (fixed)
    height: 5  (fixed)

logo_box:
    lines: 7   (fixed)
    cols: 35  (fixed)
    begin_y: 1                    (fixed)
    begin_x: screen_width - cols  (float)

side_menu_box:
    lines: logo_box.begin_y + logo_box.lines  (fixed)
    cols: 35  (fixed)
    begin_y: logo_box.begin_y + logo_box.lines  (fixed)
    begin_x: logo_box.begin_x                   (fixed)

game_box:
    lines: height - 2  (float)
    cols: width - 2    (float)
    begin_y: 1  (fixed)
    begin_x: 1  (fixed)
"""


LOGO = """
######  #####  #####   ##   ##
  ##    ##     ##  ##  ### ###
  ##    ####   ####    ## # ##
  ##    ##     ## ##   ##   ##
  ##    #####  ##  ##  ##   ##
"""


class GameEngine:
    def __init__(self, canvas):
        self.canvas = canvas
        self._setup()

    def _init_colors(self):
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

        self._draw_window_box()
        self._draw_game_box()
        self._draw_side_menu_box()
        self._draw_logo_box()
        self._draw_logo()

    def _setup_sizes(self):
        self.side_menu_box_sizes = {
            'lines': self.height - 8,
            'cols': 34,
            'begin_y': 7,
            'begin_x': self.width - 34,
        }
        self.logo_box_sizes = {
            'lines': 7,
            'cols': 34,
            'begin_y': 1,
            'begin_x': self.width - 34,
        }
        self.game_box_sizes = {
            'lines': self.height - 2,
            'cols': self.width - 34,
            'begin_y': 1,
            'begin_x': 0,
        }
        self.window_box_sizes = {
            'lines': self.height,
            'cols': self.width,
            'begin_y': 0,
            'begin_x': 0,
        }

    def _draw_window_box(self):
        box_sizes = self.window_box_sizes.values()
        self.window = curses.newwin(*box_sizes)
        self.window.nodelay(True)
        self.window.keypad(True)

    def _draw_game_box(self):
        box_sizes = self.game_box_sizes.values()
        self.game_box = self.window.subwin(*box_sizes)
        self.game_box.border()

    def _draw_side_menu_box(self):
        box_sizes = self.side_menu_box_sizes.values()
        self.side_menu_box = self.window.subwin(*box_sizes)
        self.side_menu_box.border()

    def _draw_logo_box(self):
        box_sizes = self.logo_box_sizes.values()
        self.logo_box = self.window.subwin(*box_sizes)
        self.logo_box.border()

    def _draw_logo(self):
        y, x = 1, 2

        for line in LOGO.strip('\n').split('\n'):
            self.logo_box.addstr(y, x, line)
            y += 1

        self.logo_box.addstr(6, 14, ' GAMES ')

    def _wait(self):
        """
        Using with getch() function,
        waiting for the user to press a key,
        do nothing at this moment
        """
        self.window.timeout(-1)
