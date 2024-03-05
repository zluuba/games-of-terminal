from games_of_terminal.achievements_manager import AchievementsManager
from games_of_terminal.database.database import get_games_statistic


class TicTacToeAchievementsManager(AchievementsManager):
    def has_achievement_been_unlocked(self, achievement, **kwargs):
        match achievement['name']:
            case 'Can a Robot Write a Symphony?':
                return self.check_losses_count(50)
            case 'Good Boy!':
                return self.check_wins_count(50)
            case 'Really..?':
                return self.check_total_games_count(20)
            case 'Ah Shit, Here We Go Again':
                return (self.check_total_games_count(100)
                        and self.is_game_not_over())
            case 'You Scare Me':
                return self.check_color_scheme_was_changed(**kwargs)

    def check_losses_count(self, required_quantity):
        statistic = get_games_statistic()
        losses_count = statistic[self.class_object.game_name]['total_losses']
        return losses_count >= required_quantity

    def check_wins_count(self, required_quantity):
        statistic = get_games_statistic()
        wins_count = statistic[self.class_object.game_name]['total_wins']
        return wins_count >= required_quantity

    def check_total_games_count(self, required_quantity):
        statistic = get_games_statistic()
        total_games_count = statistic[self.class_object.game_name]['total_games']
        return total_games_count >= required_quantity

    def is_game_not_over(self):
        return self.class_object.stats.game_status == 'game_active'

    @staticmethod
    def check_color_scheme_was_changed(**kwargs):
        return 'color_scheme_change' in kwargs
