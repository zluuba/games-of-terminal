from games_of_terminal.database import queries
from games_of_terminal.constants import GAMES

from sqlite3 import connect
from json import load, loads, dumps
from pathlib import Path
from os import path


def get_full_path(filename):
    return str(path.join(BASE_DIR, filename))


DB_FILENAME = 'got_games.db'
BASE_DIR = Path(__file__).parents[1]
DB_FILE_PATH = get_full_path(DB_FILENAME)

ACHIEVEMENTS_FILE = 'data/achievements.json'
ACHIEVEMENTS_FILE_PATH = get_full_path(ACHIEVEMENTS_FILE)

GAME_STATS_FILE = 'data/game_statistics.json'
GAME_STATS_FILE_PATH = get_full_path(GAME_STATS_FILE)


class Connection:
    def __init__(self, autocommit=False):
        self.autocommit = autocommit
        self.file_path = DB_FILE_PATH

    def __enter__(self):
        self.conn = connect(self.file_path)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.conn:
            return

        if self.autocommit:
            self.conn.commit()

        self.conn.close()


def check_tables_exist():
    query = queries.get_all_tables_query

    with Connection() as c:
        c.cursor.execute(query)
        existing_tables = c.cursor.fetchall()

    return len(existing_tables) == len(queries.TABLES)


def create_and_fill_db_tables():
    if check_tables_exist():
        return

    with Connection(autocommit=True) as c:
        for _, create_table_query in queries.TABLES.items():
            c.cursor.execute(create_table_query)

    add_init_stats_to_db()
    add_achievements_to_db()


def add_init_stats_to_db():
    query = queries.insert_game_stats_query

    with open(GAME_STATS_FILE_PATH, 'r') as file:
        stats_data = load(file)

    with Connection(autocommit=True) as c:
        for game_name, stats in stats_data.items():
            stats_data = dumps(stats)
            c.cursor.execute(query, (game_name, stats_data))


def add_achievements_to_db():
    with open(ACHIEVEMENTS_FILE_PATH, 'r') as file:
        achievements_data = load(file)

    with Connection(autocommit=True) as c:
        for achievements in achievements_data:
            game_name = achievements['name']
            all_achieves = achievements['achievements']

            for achievement_data in all_achieves:
                add_achievement_to_db(achievement_data, game_name, c)


def add_achievement_to_db(achievement, game_name, conn):
    achievement_name = achievement['name']
    description = achievement['description']

    conn.cursor.execute(
        queries.insert_or_ignore_achievement_query,
        (game_name, achievement_name, description),
    )


def get_game_stat(game_name, stat, unique=False):
    stat_name = 'game_stats' if unique else stat
    query = queries.get_game_stat_query(stat_name)

    with Connection() as c:
        c.cursor.execute(query, (game_name,))
        data = c.cursor.fetchone()[0]

        if not unique:
            return data

    stats_data = loads(data)
    return stats_data[stat]


def update_game_stat(game_name, stat, value, save_mode=False):
    get_query_func = queries.update_game_stat_query

    if save_mode:
        get_query_func = queries.set_game_stat_query

    query = get_query_func(stat)

    with Connection(autocommit=True) as c:
        c.cursor.execute(query, (value, game_name))


def update_game_stats(game_name, stat_name, value, save_mode=False):
    with Connection(autocommit=True) as c:
        query = queries.get_game_stat_query('game_stats')
        c.cursor.execute(query, (game_name,))
        stats_data = c.cursor.fetchone()[0]

        game_stats = loads(stats_data)

        if save_mode:
            game_stats[stat_name] = value
        else:
            game_stats[stat_name] += value

        get_query_func = queries.set_game_stat_query
        query = get_query_func('game_stats')

        game_stats = dumps(game_stats)
        c.cursor.execute(query, (game_stats, game_name))


def get_games_statistic():
    games_statistic = dict()
    query = queries.get_game_statistic_query

    with Connection() as c:
        for game_name in GAMES:
            c.cursor.execute(query, (game_name,))
            game_statistic = c.cursor.fetchall()[0]

            total_games, total_time, stats_json_data = game_statistic
            stats = loads(stats_json_data)

            games_statistic[game_name] = dict(
                total_games=total_games,
                total_time=total_time,
                **stats,
            )

    return games_statistic


def get_all_achievements():
    with Connection() as c:
        c.cursor.execute(queries.get_all_achievements_query)
        all_achievements_list = c.cursor.fetchall()

    all_achievements = dict()

    for achievement in all_achievements_list:
        game_name, name, description, status, date_received = achievement

        if game_name not in all_achievements:
            all_achievements[game_name] = []

        achievement_dict = dict(
            name=name,
            status=status,
            description=description,
            date_received=date_received,
        )
        all_achievements[game_name].append(achievement_dict)

    return all_achievements
