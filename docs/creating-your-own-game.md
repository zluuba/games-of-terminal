# How to Implement Your Own Game in GOT
If you have an idea for a game and you want to implement it, this guide is for you.  
I'll show you how to do it with an example of a 'Connect 4' game.  


1. Create a game package in 'games_of_terminal/games/' and base modules: 'core.py' and 'constants.py'. New structure:
    - 'games_of_terminal/games/connect_four/' <br/>
    - 'games_of_terminal/games/connect_four/\_\_init__.py' <br/>
    - 'games_of_terminal/games/connect_four/core.py' <br/>
    - 'games_of_terminal/games/connect_four/constants.py'

2. In 'core.py', you should write the game class (e.g., 'class ConnectFourGame(GameEngine):'). This class must inherit from 
   GameEngine found in 'games_of_terminal/games/engine.py'. The engine contains common game logic, responsible for 
   key control, pausing, restarting, providing tips, managing game status, etc., so it's **necessary**.

3. Now we should add our game to the Main Menu. Go to 'games_of_terminal/menu/constants.py', find **MENU_ITEMS**, and 
   add your game before the last one (Settings) like this: `{'name': 'Connect 4', 'class': ConnectFourGame, 'type': 'game'},`.

4. Now go to the game core ('../connect_four/core.py'), it's time to implement the base of your game. This includes a list 
   of functions that should be in the main class of the game:
   - **setup_game_stats**: This function should set all dynamic stats that should be reset when the user presses the 'Restart'
     button or ends the current game.
   - **setup_game_field**: This function should set up and draw the game window. I recommend putting 'hide_cursor' function from 
     utils (games_of_terminal/utils.py) and 'self.window.timeout(timeout)' if the game is dynamic and doesn't wait for user 
     keypress.
   - **draw_game_window**: This function should clear all windows and redraw them. It's used, for example, when an achievement
     is unlocked (this action draws the achievement animation).
   - **start_new_game**: This is the main function that starts the while loop, handles keystrokes, and controls the game process.
     This function needs to have: 'key = self.window.getch()' (and `self.wait_for_keypress()` if the game is dynamic - that
     line stops the while loop and saves your CPU resources), `self.controller(key)`, `if self.stats.is_exit or self.stats.is_restart:`,
     and `if self.is_game_over()`. See already implemented games for examples and the engine for available functions.
   - **controller**: This function processes keys that the user pressed. It should have this line: `super().controller(key, pause_on)`
     because this function was implemented in the engine and has common and required keys handlers for all games.

5. If you rebuild GOT now (using **make reinstall**), you can see your game in the Main Menu and the basic view after clicking on it.
   This means it's time to implement specific game logic. You can do it as you want. Look at GameEngine, InterfaceManager, and 
   utils.py for available functions, use 'draw_message' for item drawing on the game field, and look at other game modules. 
   Keep it clean and reusable.

6. After all, you need to add your game to the database. Edit the following files in 'games_of_terminal/data/' directory: 
   - **game_statistic.json** to add game statistics ('total_games' and 'total_time' are required);
   - **achievements.json** to add game achievements;
   - **settings.json** to add game settings; <br/>

   Then you need to add the new game to the lists that should find the game in the DB and inject the data:
   - **games_of_terminal/constants.py** file, add the game to the end of **GAMES** and **ITEMS** constants. <br/>

   Now you need to apply all changes in the database, go to the GOT -> Settings -> Reset All and reset all data.
   Now you can see your game everywhere.
   Don't forget to implement saving/getting data from the DB. See 'save_game_data' and 'apply_user_settings' functions in 
   'games_of_terminal/games/snake/core.py' for an example.

7. Done. Now you only need refactoring and manual testing (don't forget about pauses, window size changing, and so on, test it all!).
  
  
Implementing your game into GOT can seem easy, but sometimes it feels hard. And it's okay.  
Sorry for the messy codebase in some areas, I tried to do my best, but GOT still needs a lot of refactoring.  
**Thanks for your interest and good luck!**
