from games_of_terminal.achievements_manager import AchievementsManager
from games_of_terminal.database.database import get_games_statistic


class MinesweeperAchievementsManager(AchievementsManager):
    def has_achievement_been_unlocked(self, achievement):
        match achievement['name']:
            case 'Knee Shot, but Legs Saved':
                return True
            case 'RIP':
                return
            case 'Lucky':
                return self.check_bombs_defused(300)
            case 'I Have No Girlfriend':
                return self.check_bombs_defused(3000)
            case 'Skilled':
                return
            case 'That\'s Enough':
                return
            case 'Tuna':
                return

    def check_bombs_defused(self, required_quantity):
        statistic = get_games_statistic()
        bombs_defused = statistic[self.class_object.game_name]['bombs_defused']
        return bombs_defused >= required_quantity
