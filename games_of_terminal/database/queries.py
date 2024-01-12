TABLES = {
    'Games': '''
        CREATE TABLE IF NOT EXISTS Games (
            id INTEGER PRIMARY KEY,
            game_name TEXT NOT NULL,
            total_games INTEGER DEFAULT 0 NOT NULL,
            total_time INTEGER DEFAULT 0 NOT NULL,
            last_game_state TEXT DEFAULT '',
            game_stats TEXT DEFAULT ''
        );
    ''',
    'Achievements': '''
        CREATE TABLE IF NOT EXISTS Achievements (
            id INTEGER PRIMARY KEY,
            game_name TEXT NOT NULL,
            name TEXT,
            description TEXT,
            status TEXT DEFAULT 'locked',
            date_received DATE DEFAULT NULL,
            UNIQUE (name)
        );
    ''',
}

get_all_tables_query = '''
SELECT name FROM sqlite_master 
WHERE type='table';
'''

insert_or_ignore_achievement_query = '''
INSERT OR IGNORE INTO Achievements (
    game_name,
    name,
    description
)
VALUES (?, ?, ?);
'''

insert_game_stats_query = '''
INSERT INTO games (
    game_name,
    game_stats
)
VALUES (?, ?);
'''

get_game_statistic_query = '''
SELECT total_games, total_time, game_stats
FROM Games
WHERE game_name = ?;
'''

get_all_achievements_query = '''
SELECT game_name, name, description, status, date_received
FROM Achievements;
'''

update_achievements_table_query = """
"""


def get_game_stat_query(stat_name):
    return f'''
        SELECT {stat_name}
        FROM Games
        WHERE game_name = ?;
    '''


def set_game_stat_query(stat_name):
    return f'''
        UPDATE Games
        SET {stat_name} = ?
        WHERE game_name = ?;
    '''


def update_game_stat_query(stat_name):
    return f'''
        UPDATE Games
        SET {stat_name} = {stat_name} + ?
        WHERE game_name = ?;
    '''
