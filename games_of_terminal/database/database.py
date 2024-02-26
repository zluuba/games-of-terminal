from games_of_terminal.database import queries
from games_of_terminal.constants import ITEMS
from games_of_terminal.log import log
from games_of_terminal.database.constants import (
    STATISTICS_DATATYPE, SETTINGS_DATATYPE,
    DB_FILENAME, ACHIEVEMENTS_FILE,
    GAME_STATS_FILE, SETTINGS_FILE,
)

from ast import literal_eval
from collections import defaultdict
from datetime import datetime
from json import load
from os import path
from pathlib import Path
from sqlite3 import connect


def get_full_path(base_dir, filename):
    return str(path.join(base_dir, filename))


BASE_DIR = Path(__file__).parents[1]

DB_FILE_PATH = get_full_path(BASE_DIR, DB_FILENAME)
ACHIEVEMENTS_FILE_PATH = get_full_path(BASE_DIR, ACHIEVEMENTS_FILE)
GAME_STATS_FILE_PATH = get_full_path(BASE_DIR, GAME_STATS_FILE)
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
        for table_queries in queries.TABLES.values():
            create_table_query = table_queries['create_table']
            conn.cursor.execute(create_table_query)

        fill_game_table(conn)
        fill_full_game_data_table(conn)
        fill_achievement_table(conn)


def fill_game_table(conn):
    for game_name in ITEMS:
        conn.cursor.execute(queries.add_new_game_query, (game_name,))


def fill_full_game_data_table(conn):
    fill_game_data_table(conn, STATISTICS_DATATYPE, GAME_STATS_FILE_PATH)
    fill_game_data_table(conn, SETTINGS_DATATYPE, SETTINGS_FILE_PATH)


def fill_game_data_table(conn, data_type, file_path):
    with open(file_path, 'r') as file:
        data_dict = load(file)

    for game_name, data in data_dict.items():
        for name, value in data.items():
            conn.cursor.execute(
                queries.add_game_data_query,
                (game_name, data_type, name, str(value)),
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
    games_statistic[''] = {
        'all_games_played': 0,
        'time_spent_in_games': 0,
    }

    with Connection() as conn:
        conn.cursor.execute(queries.get_all_statistics_query)
        statistics_data = conn.cursor.fetchall()

    for statistics in statistics_data:
        game_name, stat_name, stat_value = statistics
        stat_value = int(stat_value)

        if stat_name == 'total_games':
            games_statistic['']['all_games_played'] += stat_value
        elif stat_name == 'total_time':
            games_statistic['']['time_spent_in_games'] += stat_value

        games_statistic[game_name][stat_name] = stat_value

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


def get_all_settings():
    all_settings = defaultdict(dict)

    with Connection() as conn:
        conn.cursor.execute(queries.get_all_settings_query)
        settings_data = conn.cursor.fetchall()

    for settings in settings_data:
        game_name, setting_name, setting_value = settings

        if setting_value and (not setting_name == 'username'):
            setting_value = literal_eval(setting_value)

        all_settings[game_name][setting_name] = setting_value

    return all_settings


def reset_all_user_data():
    with Connection(autocommit=True) as conn:
        for table_queries in queries.TABLES.values():
            drop_table_query = table_queries['drop_table']
            conn.cursor.execute(drop_table_query)

    create_and_fill_db_tables()


def get_username():
    with Connection() as conn:
        conn.cursor.execute(queries.get_username_query)
        username = conn.cursor.fetchone()

    return username[0]


def save_username(username):
    with Connection(autocommit=True) as conn:
        conn.cursor.execute(queries.save_username_query, (username,))


def unlock_achievement(game_name, achievement_name):
    current_date = datetime.today().strftime('%d.%m.%Y')

    with Connection(autocommit=True) as conn:
        conn.cursor.execute(queries.unlock_achievement_query,
                            (current_date, game_name, achievement_name,))


def save_selected_option(game_name, option_name, chosen_item):
    with Connection(autocommit=True) as conn:
        conn.cursor.execute(queries.get_option_query,
                            (game_name, option_name))
        options = conn.cursor.fetchone()[0]
        options_list = literal_eval(options)

        # unselect current and select chosen item
        for option in options_list:
            if option['selected']:
                option['selected'] = False
            if option['name'] == chosen_item:
                option['selected'] = True

        conn.cursor.execute(queries.update_option_query,
                            (str(options_list), game_name, option_name))
