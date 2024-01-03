from games_of_terminal.database import queries

from sqlite3 import connect
from json import load
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
    with Connection() as c:
        c.cursor.execute(queries.get_all_tables_query)
        existing_tables = c.cursor.fetchall()
        return len(existing_tables) == len(queries.TABLES)


def create_and_fill_db_tables():
    if check_tables_exist():
        return

    with Connection(autocommit=True) as c:
        for _, create_table_query in queries.TABLES.items():
            c.cursor.execute(create_table_query)

    add_achievements_to_db()


def add_achievements_to_db():
    with open(ACHIEVEMENTS_FILE_PATH, 'r') as file:
        achievements_data = load(file)

    with Connection(autocommit=True) as c:
        for achievements in achievements_data:
            item_name = achievements['name']
            all_achieves = achievements['achievements']

            for achievement_data in all_achieves:
                add_achievement_to_db(
                    achievement_data,
                    item_name,
                    c,
                )


def add_achievement_to_db(achievement, game_name, conn):
    achievement_name = achievement['name']
    description = achievement['description']
    status = achievement['status']

    conn.cursor.execute(
        queries.insert_or_ignore_achievement_query,
        (game_name, achievement_name, description, status),
    )


def get_game_state(game_name, stat):
    with Connection() as c:
        query = queries.get_game_state_query(game_name, stat)
        c.cursor.execute(query)
        data = c.cursor.fetchone()
        return data[0]


def update_game_state(game_name, stat, value, save_mode=False):
    get_query_func = queries.update_game_state_query

    if save_mode:
        get_query_func = queries.set_game_state_query

    query = get_query_func(game_name, stat)

    with Connection(autocommit=True) as c:
        c.cursor.execute(query, (value,))
