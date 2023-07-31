import curses


class GameEngine:
    def __init__(self, canvas):
        self.canvas = canvas
        self._setup()

    def _init_colors(self):
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)     # black
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)     # green
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)       # red
        curses.init_pair(4, 1, 236)                                     # dark grey

    def _setup(self):
        self.height, self.width = self.canvas.getmaxyx()
        self.canvas.bkgd(' ', curses.color_pair(1))

        self._setup_game_window()
        self._init_colors()

    def _setup_game_window(self):
        self.window = curses.newwin(self.height - 2, self.width - 2, 1, 1)
        self.window.nodelay(True)
        self.window.keypad(True)
        self.window.border()

    def _wait(self):
        """
        Using with getch() function,
        waiting for the user to press a key,
        do nothing at this moment
        """
        self.window.timeout(-1)
