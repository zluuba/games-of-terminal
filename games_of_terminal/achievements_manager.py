from games_of_terminal.database.database import get_all_achievements, unlock_achievement


class AchievementsManager:
    def __init__(self, class_object):
        self.class_object = class_object
        self.achievements = self.get_locked_achievements()

    def get_locked_achievements(self):
        all_achievements = get_all_achievements()
        locked_achievements = []

        for game_name, achievements in all_achievements.items():
            if self.class_object.game_name != game_name:
                continue

            for achievement in achievements:
                if achievement['status'] == 'locked':
                    locked_achievements.append(achievement)

        return locked_achievements

    def check(self):
        for achievement in self.achievements:
            if self.has_achievement_been_unlocked(achievement):
                self.unlock_achievement(achievement)

    def unlock_achievement(self, achievement):
        unlock_achievement(self.class_object.game_name, achievement['name'])
        self.notify_user(achievement)
        self.achievements = self.get_locked_achievements()

    def notify_user(self, achievement):
        pass

    def has_achievement_been_unlocked(self, achievement):
        pass
