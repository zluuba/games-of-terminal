from games_of_terminal.achievements_manager import AchievementsManager
from games_of_terminal.database.database import get_games_statistic


class SnakeGameAchievementsManager(AchievementsManager):
    def has_achievement_been_unlocked(self, achievement):
        match achievement['name']:
            case 'Answer Seeker':
                return self.check_score(42)
            case 'Are you okay?':
                return self.check_score(101)
            case 'Ten Out of Ten':
                return self.check_total_games_count(10)
            case 'The Grass Must Be Touched':
                return self.check_total_games_count(75)
            case 'Good Soup':
                return self.class_object.is_snake_eat_itself()
            case 'Fashionista':
                return
            case 'Mode Mood':
                return
            case 'GOD':
                return

    def check_score(self, required_quantity):
        return self.class_object.stats.score >= required_quantity

    def check_total_games_count(self, required_quantity):
        statistic = get_games_statistic()
        total_games_count = statistic[self.class_object.game_name]['total_games']
        return total_games_count >= required_quantity
