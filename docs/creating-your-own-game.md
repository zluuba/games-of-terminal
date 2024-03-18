# How to implement in GOT you own game
If you have an idea for a game, and you want to implement it, this guide for you.  
I'll show you how to do it with an example of a 'Connect 4' game.   


1. Create game package in 'games_of_terminal/games/' and base modules: 'core.py' and 'constants.py'. New structure:
        -> 'games_of_terminal/games/connect_four/'
        -> 'games_of_terminal/games/connect_four/__init__.py'
        -> 'games_of_terminal/games/connect_four/core.py'
        -> 'games_of_terminal/games/connect_four/constants.py'
2. In 'core.py' file you should write game class (ex: 'class ConnectFourGame(GameEngine):'). This class must inherit from 
   GameEngine from 'games_of_terminal/games/engine.py'. Engine have common games logic, responsible for the 
   pressed keys controller, pause, restart, tips, game status, etc., so it's **necessary**.
3. Now we should add our game to the Main Menu. Go to the 'games_of_terminal/menu/constants.py', find 'MENU_ITEMS' and 
   add your game before the last one (Settings) like that: '{'name': 'Connect 4', 'class': ConnectFourGame, 'type': 'game'},'.
4. Now go to the game core ('../connect_four/core.py'), it's time to implement the base of you game. This is list 
   of functions, that should be in main class of the game:
        - 'setup_game_stats' - this function should set all dynamic stats that should be reset when user press 'Restart'
           button, or end current game.
        - 'setup_game_field' - should set up and draw game window. I recommend put there 'hide_cursor' func from utils
           (games_of_terminal/utils.py) and 'self.window.timeout(timeout)' if game is dynamic and don't wait for user keypress.
        - 'draw_game_window' - should clear all windows and redraw them. This function used, for example, when achievement
           was unlocked (this action draw achievement animation).
        - 'start_new_game' - main function, which start while loop, handles keystrokes and controls the game process.
           This function need to have: 'key = self.window.getch()' (and self.wait_for_keypress() if game is dynamic - that
           line stop while loop and save your CPU resources), 'self.controller(key)', 'if self.stats.is_exit or self.stats.is_restart:'
           and 'if self.is_game_over():'. See already implemented games for examples. And engine for available functions.
        - 'controller' - processed keys that user pressed. Should have this line 'super().controller(key, pause_on)'
           because this function was implemented in engine and have common and required for all games keys handlers.
5. If you rebuild GOT now (using **make reinstall**), you can see your game in Main Menu and base view after clicking on it.
   That's mean that it's time for implement specific game logic. You can do it like you want. Look at GameEngine,
   InterfaceManager and utils.py for available functions, use 'draw_message' for items drawing on the game field and
   look at other games modules. Keep it clean and reusable.
6. After all you need to add your game to database. Edit next files: 
        -> 'games_of_terminal/data/game_statistic.json' to add game statistic ('total_games' and 'total_time' is required)
        -> 'games_of_terminal/data/achievements.json' to add game achievements.
        -> 'games_of_terminal/data/settings.json' to add game settings.
   Then you need to add new game to the lists, that should find game in DB and inject the data:
        -> 'games_of_terminal/constants.py' file, add game to the end of GAMES and ITEMS constants.
   Now you need to apply all changes in database, go to the GOT -> Settings -> Reset All.
   Done, now you can see you game everywhere.
   Don't forget to implement saving/getting data from DB. See 'save_game_data' and 'apply_user_settings' functions in 
   'games_of_terminal/games/snake/core.py' for example.
7. Done. Now you need only refactoring and manual testing (don't forget about pauses, window size changing and so on, test it all!).
  
  
Implementing your game into GOT can seem easy, but sometimes it's feels hard. And it's okay.  
Sorry for garbage codebase somewhere, I tried to do my best, but GOT still needs a lot of refactoring.  
Thanks for your interest and good luck!
