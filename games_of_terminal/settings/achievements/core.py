from games_of_terminal.interface_manager import InterfaceManager


class Achievements(InterfaceManager):
    def __init__(self, canvas, settings_name):
        super().__init__(canvas)
        self.settings_name = settings_name

    def run(self):
        pass
