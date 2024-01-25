from games_of_terminal.database import queries
from games_of_terminal.constants import ITEMS
from games_of_terminal.log import log

from collections import defaultdict
from json import load
from os import path
from pathlib import Path
from sqlite3 import connect


def get_full_path(base_dir, filename):
    return str(path.join(base_dir, filename))


DB_FILENAME = 'got_games.db'
BASE_DIR = Path(__file__).parents[1]
DB_FILE_PATH = get_full_path(BASE_DIR, DB_FILENAME)

ACHIEVEMENTS_FILE = 'data/achievements.json'
ACHIEVEMENTS_FILE_PATH = get_full_path(BASE_DIR, ACHIEVEMENTS_FILE)

GAME_STATS_FILE = 'data/game_statistics.json'
GAME_STATS_FILE_PATH = get_full_path(BASE_DIR, GAME_STATS_FILE)

SETTINGS_FILE = 'data/settings.json'
SETTINGS_FILE_PATH = get_full_path(BASE_DIR, SETTINGS_FILE)


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


@log
def check_tables_exist():
    query = queries.get_all_tables_query

    with Connection() as c:
        c.cursor.execute(query)
        existing_tables = c.cursor.fetchall()

    return len(existing_tables) == len(queries.TABLES)


@log
def create_and_fill_db_tables():
    if check_tables_exist():
        return

    with Connection(autocommit=True) as conn:
        for create_table_query in queries.TABLES.values():
            conn.cursor.execute(create_table_query)

        fill_game_table(conn)
        fill_full_game_data_table(conn)
        fill_achievement_table(conn)


def fill_game_table(conn):
    for game_name in ITEMS:
        conn.cursor.execute(
            queries.add_new_game_query,
            (game_name,)
        )


def fill_full_game_data_table(conn):
    fill_game_data_table(conn, 'statistics', GAME_STATS_FILE_PATH)
    fill_game_data_table(conn, 'settings', SETTINGS_FILE_PATH)


def fill_game_data_table(conn, data_type, file_path):
    with open(file_path, 'r') as file:
        data_dict = load(file)

    for game_name, data in data_dict.items():
        for name, value in data.items():
            conn.cursor.execute(
                queries.add_game_data_query,
                (game_name, data_type, name,
                 str(value))
            )


def fill_achievement_table(conn):
    with open(ACHIEVEMENTS_FILE_PATH, 'r') as file:
        games_achievements_data = load(file)

    for game in games_achievements_data:
        for achievement in game['achievements']:
            conn.cursor.execute(
                queries.add_achievement_query,
                (game['name'], achievement['name'],
                 achievement['description'])
            )


@log
def get_game_stat_value(game_name, stat_name, data_type='statistics'):
    with Connection() as conn:
        conn.cursor.execute(
            queries.get_game_stat_query,
            (game_name, data_type, stat_name))
        value = conn.cursor.fetchone()[0]

    return value


@log
def update_game_stat(game_name, stat_name, value,
                     data_type='statistics',
                     save_mode=False):
    if save_mode:
        query = queries.set_game_stat_query
    else:
        query = queries.increase_game_stat_query

    with Connection(autocommit=True) as conn:
        conn.cursor.execute(
            query,
            (str(value), game_name, data_type, stat_name)
        )


def get_games_statistic():
    games_statistic = defaultdict(dict)

    with Connection() as conn:
        conn.cursor.execute(queries.get_all_statistics_query)
        statistics_data = conn.cursor.fetchall()

        for statistics in statistics_data:
            game_name, stat_name, value = statistics
            games_statistic[game_name][stat_name] = int(value)

    return games_statistic


def get_all_achievements():
    all_achievements = defaultdict(list)

    with Connection() as conn:
        conn.cursor.execute(queries.get_all_achievements_query)
        all_achievements_list = conn.cursor.fetchall()

    for achievement in all_achievements_list:
        game_name, name, description, status, date_received = achievement
        all_achievements[game_name].append(dict(
            name=name,
            status=status,
            description=description,
            date_received=date_received,
        ))

    return all_achievements
