from games_of_terminal.settings.placeholder_stub import PlaceholderStub
from games_of_terminal.app_interface import InterfaceManager
import time


class ConfessAll(InterfaceManager):
    def __init__(self, canvas, settings_name):
        super().__init__(canvas)
        self.settings_name = settings_name
        self.placeholder_stub = PlaceholderStub(
            self.height, self.width,
            self.window, self.default_color,
        )

    def run(self):
        self.hide_cursor()
        self.placeholder_stub.show_stub()

        time.sleep(1)
