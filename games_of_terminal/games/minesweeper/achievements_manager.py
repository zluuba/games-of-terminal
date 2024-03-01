from games_of_terminal.achievements_manager import AchievementsManager
from games_of_terminal.database.database import get_games_statistic


class MinesweeperAchievementsManager(AchievementsManager):
    def has_achievement_been_unlocked(self, achievement, **kwargs):
        match achievement['name']:
            case 'Knee Shot, but Legs Saved':
                return self.check_first_win()
            case 'RIP':
                return self.check_first_death()
            case 'Lucky':
                return self.check_bombs_defused(300)
            case 'I Have No Girlfriend':
                return self.check_bombs_defused(3000)
            case 'Skilled':
                return self.is_there_six_plus_bombs_around_one_cell()
            case 'That\'s Enough':
                return self.check_extra_place_flag_attempt(**kwargs)
            case 'Tuna':
                return self.check_color_scheme_was_changed(**kwargs)

    def check_bombs_defused(self, required_quantity):
        statistic = get_games_statistic()
        bombs_defused = statistic[self.class_object.game_name]['bombs_defused']
        return bombs_defused >= required_quantity

    def check_first_win(self):
        statistic = get_games_statistic()
        wins_count = statistic[self.class_object.game_name]['total_wins']
        return wins_count >= 1

    def check_first_death(self):
        statistic = get_games_statistic()
        losses_count = statistic[self.class_object.game_name]['total_losses']
        return losses_count >= 1

    def is_there_six_plus_bombs_around_one_cell(self):
        if self.class_object.stats.game_status != 'user_win':
            return

        for cell in self.class_object.cells.values():
            if cell.bombs_around >= 6:
                return True
        return False

    @staticmethod
    def check_extra_place_flag_attempt(**kwargs):
        return 'extra_flag' in kwargs

    @staticmethod
    def check_color_scheme_was_changed(**kwargs):
        return 'color_scheme_change' in kwargs
