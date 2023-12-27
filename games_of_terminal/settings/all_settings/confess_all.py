from games_of_terminal.settings.placeholder_stub import show_placeholder_stub
from games_of_terminal.app_interface import InterfaceManager
from games_of_terminal.constants import DEFAULT_COLOR
import time


class ConfessAll(InterfaceManager):
    def __init__(self, canvas, settings_name):
        super().__init__(canvas)
        self.settings_name = settings_name

    def run(self):
        show_placeholder_stub(
            self.height, self.width,
            self.window, DEFAULT_COLOR,
        )

        time.sleep(1)
