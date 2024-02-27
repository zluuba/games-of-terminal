from games_of_terminal.achievements_manager import AchievementsManager
from games_of_terminal.database.database import get_games_statistic


class TetrisAchievementsManager(AchievementsManager):
    def has_achievement_been_unlocked(self, achievement, **kwargs):
        match achievement['name']:
            case 'It Was.. Fast.':
                return self.check_first_death()
            case 'Cubie':
                return self.check_score(20_000)
            case 'Yoda':
                return self.check_score(100_000)
            case 'You Beat Me!':
                return self.check_score(339_500)
            case 'Did You See The Movie?':
                return self.check_lines_remove_count(10)
            case 'Annihilator':
                return
            case 'Void':
                return
            case 'Nitrous':
                return

    def check_first_death(self):
        statistic = get_games_statistic()
        losses_count = statistic[self.class_object.game_name]['total_losses']
        return losses_count == 1

    def check_score(self, required_quantity):
        return self.class_object.stats.score >= required_quantity

    def check_lines_remove_count(self, required_quantity):
        return self.class_object.lines_removed >= required_quantity

    def check_wins_count(self, required_quantity):
        statistic = get_games_statistic()
        wins_count = statistic[self.class_object.game_name]['total_wins']
        return wins_count >= required_quantity

    def check_total_games_count(self, required_quantity):
        statistic = get_games_statistic()
        total_games_count = statistic[self.class_object.game_name]['total_games']
        return total_games_count >= required_quantity

    @staticmethod
    def check_color_scheme_was_changed(**kwargs):
        if 'color_scheme_change' in kwargs:
            return True
        return False
