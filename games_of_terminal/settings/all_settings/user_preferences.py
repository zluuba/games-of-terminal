from games_of_terminal.app_interface import InterfaceManager
from games_of_terminal.constants import DEFAULT_COLOR
from games_of_terminal.utils import show_placeholder_stub
import time


class UserPreferences(InterfaceManager):
    def __init__(self, canvas, settings_name):
        super().__init__(canvas)
        self.settings_name = settings_name

    def run(self):
        show_placeholder_stub(
            self.height, self.width,
            self.window, DEFAULT_COLOR,
        )

        time.sleep(1)
