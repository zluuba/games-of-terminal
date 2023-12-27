from games_of_terminal.app_interface import InterfaceManager
# from games_of_terminal.menu.constants import MENU_ITEMS


class Statistics(InterfaceManager):
    def __init__(self, canvas, settings_name):
        super().__init__(canvas)
        self.settings_name = settings_name

    def run(self):
        pass


logic = """
Game Played: int
Total Time Played: int

Snake Game
    Total Games: int
    Total Time: int
    Best Score: int
    Achievements Unlocked: int / int

Minesweeper Game
    Total Games: int
    Total Time: int
    Total Wins: int
    Total Loses: int
    Bombs Defused: int
    Achievements Unlocked: int / int

TicTacToe Game
    Total Games: int
    Total Time: int
    Lines Removed: int
    Total Wins: int
    Total Loses: int
    Total Ties: int
    Achievements Unlocked: int / int

Tetris Game
    Total Games: int
    Total Time: int
    Best Score: int
    Achievements Unlocked: int / int
"""
