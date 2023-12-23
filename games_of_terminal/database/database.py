from games_of_terminal.database.queries import *
from games_of_terminal.database.achievements import achievements
from pathlib import Path
from os import path
import sqlite3


DB_FILENAME = 'got_games.db'
BASE_DIR = Path(__file__).parents[1]
FILE_PATH = path.join(BASE_DIR, DB_FILENAME)

# TODO: try SQL builder


def create_connection():
    return sqlite3.connect(FILE_PATH)


def get_connection_and_cursor():
    connection = create_connection()
    cursor = connection.cursor()
    return connection, cursor


def check_tables_exist():
    conn, cursor = get_connection_and_cursor()
    cursor.execute(get_all_tables_query)
    existing_tables = cursor.fetchall()
    return len(existing_tables) == len(TABLES)


def create_db_tables():
    if check_tables_exist():
        return

    conn, cursor = get_connection_and_cursor()

    for _, create_table_query in TABLES.items():
        cursor.execute(create_table_query)

    cursor.execute(insert_default_games_query)

    for achievement_name, (description, game) in achievements.items():
        cursor.execute(get_game_id_query, (game,))
        data = cursor.fetchone()

        game_id = data[0]
        cursor.execute(
            insert_achievements_query,
            (game_id, achievement_name, description)
        )

    conn.commit()
    conn.close()


def get_game_state(game_name, stat):
    conn, cursor = get_connection_and_cursor()

    query = get_game_state_query(stat)
    cursor.execute(query, (game_name,))
    data = cursor.fetchone()
    conn.close()
    return data[0]


def save_game_state(game_name, stat, value):
    conn, cursor = get_connection_and_cursor()
    query = set_game_state_query(stat)
    cursor.execute(query, (value, game_name))

    conn.commit()
    conn.close()


def update_game_state(game_name, stat, value):
    # same as save_game_state. bring them together
    conn, cursor = get_connection_and_cursor()
    query = update_game_state_query(stat)
    cursor.execute(query, (value, game_name))

    conn.commit()
    conn.close()
