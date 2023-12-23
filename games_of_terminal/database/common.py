create_game_table_query = '''
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY,
    game_name TEXT,
    total_wins INTEGER DEFAULT 0 NOT NULL,
    total_losses INTEGER DEFAULT 0 NOT NULL,
    total_ties INTEGER DEFAULT 0 NOT NULL,
    total_time INTEGER DEFAULT '00:00' NOT NULL,
    best_time INTEGER DEFAULT '00:00' NOT NULL,
    best_score INTEGER DEFAULT 0 NOT NULL,
    last_game TEXT DEFAULT ''
);
'''

create_achievements_table_query = '''
CREATE TABLE IF NOT EXISTS achievements (
    id INTEGER PRIMARY KEY,
    game_id INTEGER,
    achievement_name TEXT,
    achievement_description TEXT,
    date_received DATE,
    FOREIGN KEY (game_id) REFERENCES games(id)
);
'''

get_all_tables_query = '''
SELECT name FROM sqlite_master 
WHERE type='table' AND name IN ('games', 'achievements');
'''

insert_default_games_query = '''
INSERT INTO games (game_name) VALUES
    ('Tetris'),
    ('Minesweeper'),
    ('TicTacToe'),
    ('Snake');
'''

insert_achievements_query = '''
INSERT INTO achievements (
    game_id,
    achievement_name, 
    achievement_description, 
    date_received
)
VALUES (?, ?, ?, NULL);
'''

get_game_id_query = '''
SELECT id FROM games WHERE game_name = ?;
'''

get_game_state_query = lambda stat_name: (
    f'''
    SELECT {stat_name}
    FROM games
    WHERE game_name = ?;
    '''
)

set_game_state_query = lambda stat_name: (
    f'''
    UPDATE games
    SET {stat_name} = ?
    WHERE game_name = ?;
    '''
)

update_game_state_query = lambda stat_name: (
    f'''
    UPDATE games
    SET {stat_name} = {stat_name} + ?
    WHERE game_name = ?;
    '''
)

TABLES = {
    'games': create_game_table_query,
    'achievements': create_achievements_table_query,
}

# temporary
achievements = {
    'Achievement1': ('Description for Achievement1', 'Snake'),
    'Achievement2': ('Description for Achievement2', 'Tetris'),
}
