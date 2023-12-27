from games_of_terminal.database.queries import *
from games_of_terminal.database.achievements import achievements
from pathlib import Path
from os import path
import sqlite3


DB_FILENAME = 'got_games.db'
BASE_DIR = Path(__file__).parents[1]
FILE_PATH = path.join(BASE_DIR, DB_FILENAME)


class Connection:
    def __init__(self, autocommit=False):
        self.autocommit = autocommit
        self.file_path = FILE_PATH

    def __enter__(self):
        self.conn = sqlite3.connect(self.file_path)
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
        c.cursor.execute(get_all_tables_query)
        existing_tables = c.cursor.fetchall()
        return len(existing_tables) == len(TABLES)


def create_db_tables():
    if check_tables_exist():
        return

    with Connection(autocommit=True) as c:
        for _, create_table_query in TABLES.items():
            c.cursor.execute(create_table_query)

        c.cursor.execute(insert_default_games_query)

        for achievement_name, (description, game) in achievements.items():
            c.cursor.execute(get_game_id_query, (game,))
            data = c.cursor.fetchone()

            game_id = data[0]
            c.cursor.execute(
                insert_achievements_query,
                (game_id, achievement_name, description)
            )


def get_game_state(game_name, stat):
    with Connection() as c:
        query = get_game_state_query(stat)
        c.cursor.execute(query, (game_name,))
        data = c.cursor.fetchone()
        return data[0]


def update_game_state(game_name, stat, value, save_mode=False):
    get_query = set_game_state_query if save_mode else update_game_state_query
    query = get_query(stat)

    with Connection(autocommit=True) as c:
        c.cursor.execute(query, (value, game_name))
