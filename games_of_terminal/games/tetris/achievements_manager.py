from games_of_terminal.achievements_manager import AchievementsManager
from games_of_terminal.database.database import get_games_statistic

from .constants import LEVELS


class TetrisAchievementsManager(AchievementsManager):
    def has_achievement_been_unlocked(self, achievement, **kwargs):
        match achievement['name']:
            case 'It Was.. Fast.':
                return self.check_first_death()
            case 'Cubie':
                return self.check_score(50_000)
            case 'Yoda':
                return self.check_score(100_000)
            case 'You Beat Me!':
                return self.check_score(339_500)
            case 'Did You See The Movie?':
                return self.check_lines_remove_count(10)
            case 'Annihilator':
                return self.check_user_clear_four_lines_at_once(**kwargs)
            case 'Void':
                return self.check_field_was_cleared()
            case 'Nitrous':
                return self.check_last_block_speed_level_was_reached()

    def check_first_death(self):
        statistic = get_games_statistic()
        losses_count = statistic[self.class_object.game_name]['total_games']
        return losses_count >= 1

    def check_score(self, required_quantity):
        return self.class_object.stats.score >= required_quantity

    def check_lines_remove_count(self, required_quantity):
        return self.class_object.lines_removed >= required_quantity

    @staticmethod
    def check_color_scheme_was_changed(**kwargs):
        return 'color_scheme_change' in kwargs

    @staticmethod
    def check_user_clear_four_lines_at_once(**kwargs):
        return 'four_lines_removing' in kwargs

    def check_field_was_cleared(self):
        return ((not self.class_object.board.landed_blocks) and
                (self.class_object.stats.score > 0))

    def check_last_block_speed_level_was_reached(self):
        return self.class_object.level == max(LEVELS.keys())
