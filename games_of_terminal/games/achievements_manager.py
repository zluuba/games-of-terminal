from games_of_terminal.database.database import (
    get_games_statistic, get_all_achievements,
)


class GlobalAchievementsManager:
    def has_achievement_been_unlocked(self, achievement, **kwargs):
        match achievement['name']:
            case 'Gamer':
                return self.check_all_games_was_played()
            case 'Better Than Sex':
                return self.check_time_in_games(3_600)
            case 'Game-a-holic':
                return self.check_games_played_count(50)
            case '666 Days of Darkness':
                return self.check_games_played_count(666)
            case 'How You Doin\'? ;)':
                return self.check_username_was_changed(**kwargs)
            case 'Nice!':
                return self.check_confess_option_was_found(**kwargs)
            case 'Ctrl + Alt + Achieve':
                return self.check_unlocked_ach_count(20)
            case 'Creator\'s Favorite':
                all_achievements_count = self.get_all_achievements_count()
                required_quantity = all_achievements_count - 1
                return self.check_unlocked_ach_count(required_quantity)

    @staticmethod
    def check_all_games_was_played():
        statistic = get_games_statistic()
        del statistic['']

        return all(map(lambda stats: stats['total_games'],
                       statistic.values()))

    @staticmethod
    def check_time_in_games(required_quantity):
        statistic = get_games_statistic()
        return statistic['']['time_spent_in_games'] >= required_quantity

    @staticmethod
    def check_games_played_count(required_quantity):
        statistic = get_games_statistic()
        return statistic['']['all_games_played'] >= required_quantity

    @staticmethod
    def check_username_was_changed(**kwargs):
        return 'username_change' in kwargs

    @staticmethod
    def check_confess_option_was_found(**kwargs):
        return 'confess_option' in kwargs

    @staticmethod
    def check_unlocked_ach_count(required_quantity):
        achievements = get_all_achievements()
        unlocked_ach_count = 0

        for game_achievements in achievements.values():
            for achievement in game_achievements:
                if achievement['status'] == 'unlocked':
                    unlocked_ach_count += 1

        return unlocked_ach_count >= required_quantity

    @staticmethod
    def get_all_achievements_count():
        achievements = get_all_achievements()
        return sum(map(lambda game_ach: len(game_ach),
                       achievements.values()))
