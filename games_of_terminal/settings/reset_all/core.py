from games_of_terminal.interface_manager import InterfaceManager
from games_of_terminal.utils import show_placeholder_stub

import time


class ResetAll(InterfaceManager):
    def __init__(self, canvas, name):
        super().__init__(canvas)
        self.name = name

    def run(self):
        show_placeholder_stub(self.height, self.width, self.window)
        time.sleep(1)
