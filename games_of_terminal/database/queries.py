TABLES = {
    'game': '''
        CREATE TABLE IF NOT EXISTS game (
            id_game INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );
    ''',
    # data_type: statistics, settings
    'game_data': '''
        CREATE TABLE IF NOT EXISTS game_data (
            id_game_data INTEGER PRIMARY KEY,
            id_game INTEGER NOT NULL DEFAULT 0,
            data_type TEXT NOT NULL,
            name TEXT NOT NULL,
            value TEXT,
            FOREIGN KEY (id_game) REFERENCES game(id_game)
        );
    ''',
    'achievement': '''
        CREATE TABLE IF NOT EXISTS achievement (
            id_achievement INTEGER PRIMARY KEY,
            id_game INTEGER NULL,
            name TEXT UNIQUE NOT NULL,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'locked',
            date_received TEXT NULL,
            FOREIGN KEY (id_game) REFERENCES game(id_game)
        );
    ''',
}

get_all_tables_query = '''
SELECT name
FROM sqlite_master 
WHERE type='table';
'''

get_game_id_by_game_name_query = '''
SELECT id_game
FROM game 
WHERE name = ?;
'''

add_new_game_query = '''
INSERT INTO game (
    name
)
VALUES (?);
'''

add_game_data_query = '''
INSERT INTO game_data (
    id_game,
    data_type,
    name,
    value
)
VALUES ((SELECT id_game FROM game WHERE name = ?), ?, ?, ?);
'''

get_game_data_query = '''
SELECT name, 
       value
FROM game_data
WHERE id_game = ? AND data_type = ?;
'''

get_game_stat_query = '''
SELECT game_data.value
FROM game_data
JOIN game ON game_data.id_game = game.id_game
WHERE game.name = ? 
    AND game_data.data_type = ? 
    AND game_data.name = ?;
'''

set_game_stat_query = '''
UPDATE game_data
SET value = ?
WHERE id_game IN (SELECT id_game FROM game WHERE name = ?)
    AND data_type = ?
    AND name = ?;
'''

increase_game_stat_query = '''
UPDATE game_data
SET value = value + ?
WHERE id_game IN (SELECT id_game FROM game WHERE name = ?)
    AND data_type = ?
    AND name = ?;
'''

get_all_statistics_query = '''
SELECT game.name as game_name, 
       game_data.name, 
       game_data.value
FROM game_data
JOIN game ON game_data.id_game = game.id_game
WHERE game_data.data_type = 'statistics'; 
'''

add_achievement_query = '''
INSERT INTO achievement (
    id_game,
    name,
    description
)
VALUES ((SELECT id_game FROM game WHERE name = ?), ?, ?);
'''

get_all_achievements_query = '''
SELECT game.name as game_name, 
       achievement.name, 
       achievement.description, 
       achievement.status, 
       achievement.date_received
FROM achievement
JOIN game ON achievement.id_game = game.id_game;
'''
