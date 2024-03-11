from games_of_terminal.achievements_manager import AchievementsManager
from games_of_terminal.database.database import get_games_statistic


class SnakeGameAchievementsManager(AchievementsManager):
    def has_achievement_been_unlocked(self, achievement, **kwargs):
        match achievement['name']:
            case 'Normal Size Snake':
                return self.check_score(15)
            case 'Answer Seeker':
                return self.check_score(42)
            case 'Are You Okay?':
                return self.check_score(101)
            case 'Wait.. What?':
                return self.check_score(321)
            case 'Ten Out of Ten':
                return self.check_total_games_count(10)
            case 'The Grass Must Be Touched':
                return self.check_total_games_count(75)
            case 'Good Soup':
                return self.class_object.is_snake_eat_itself()
            case 'Fashionista':
                return self.check_snake_color_scheme_was_changed(**kwargs)
            case 'Mode Mood':
                return self.check_game_mode_was_changed(**kwargs)
            case 'GOD':
                return self.check_user_win()

    def check_score(self, required_quantity):
        return self.class_object.stats.score >= required_quantity

    def check_total_games_count(self, required_quantity):
        statistic = get_games_statistic()
        game_statistic = statistic[self.class_object.game_name]
        total_games_count = game_statistic['total_games']
        return total_games_count >= required_quantity

    def check_user_win(self):
        return self.class_object.stats.game_status == 'user_win'

    @staticmethod
    def check_snake_color_scheme_was_changed(**kwargs):
        return 'snake_color_scheme_change' in kwargs

    @staticmethod
    def check_game_mode_was_changed(**kwargs):
        return 'game_mode_change' in kwargs
