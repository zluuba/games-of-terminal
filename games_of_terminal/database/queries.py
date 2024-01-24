TABLES = {
    'game': '''
        CREATE TABLE IF NOT EXISTS game (
            id_game INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );
    ''',
    # data_type - achievement, statistic, setting
    'game_data': '''
        CREATE TABLE IF NOT EXISTS game_data (
            id_game_data INTEGER PRIMARY KEY,
            id_game INTEGER,
            data_type TEXT NOT NULL,
            name TEXT NOT NULL,
            value TEXT NOT NULL,
            value_type TEXT NOT NULL,
            FOREIGN KEY (game_id) REFERENCES game(id_game)
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
            global INTEGER DEFAULT 0,
            FOREIGN KEY (game_id) REFERENCES game(id_game)
        );
    ''',
}

get_all_tables_query = '''
SELECT name FROM sqlite_master 
WHERE type='table';
'''

insert_game_achievement_query = '''
INSERT INTO achievement (
    id_game,
    name,
    description
)
VALUES (?, ?, ?);
'''

insert_global_achievement_query = '''
INSERT INTO achievement (
    name,
    description,
    global
)
VALUES (?, ?, ?);
'''

get_game_data_query = '''
SELECT name, value, value_type
FROM game_data
WHERE id_game = ? AND data_type = ?;
'''

get_all_achievements_query = '''
SELECT 
    game.name as game_name, 
    achievement.name, 
    achievement.description, 
    achievement.status, 
    achievement.date_received, 
    achievement.global
FROM achievement
JOIN game ON achievement.id_game = game.id_game;
'''

get_game_stat_query = '''
SELECT game_data.value, game_data.value_type
FROM game_data
JOIN game ON game_data.id_game = game.id_game
WHERE game.name = ? 
    AND game_data.data_type = ? 
    AND game_data.name = ?;
'''

set_game_stat_query = '''
UPDATE game_data
SET value = ?, value_type = ?
WHERE id_game IN (SELECT id_game FROM game WHERE name = ?)
    AND data_type = ?
    AND name = ?;
'''
