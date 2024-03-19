# Technical Details of GOT
Here are some details for understanding the codebase and project structure.

## Project Structure
I've tried to separate all main parts, so this is the abstract structure of the whole app:

```plaintext
    . Main Module of GOT
    |__ Scripts (main script that runs the Main Menu)
    |__ Main Menu
    |__ Games
        |__ Games Engine (file)
        |__ Snake Game
        |__ Tetris Game
        |__ ...
    |__ Settings
        |__ Achievements
        |__ Games Settings
        |__ Games Statistics
        |__ Reset All Data
        |__ Share Data
    |__ Static Data (achievements, settings, game stats in .json format)
    |__ Database
    |__ Interface Manager (file)
    |__ Achievements Manager (file)
    |__ Utils (file)
    |__ Logger (file)
```

## Documentation
### Interface Manager

The file './games_of_terminal/interface_manager.py' contains the **InterfaceManager class**, which is responsible for 
setting up working windows. If you initialize your InterfaceManager with `only_main_win=True` in your `__init__` method 
(like this: `super().__init__(canvas, only_main_win=True)`), you will have access to `self.window` in your game class. 
Otherwise, you would have access to `self.window, self.game_area, self.side_menu, self.tips_area, self.logo_area`, 
and `self.game_status_area`. The first option, with only the main window, is used in menus and settings, 
while the latter is used for games.
  
The InterfaceManager class has the following methods:

- **\_setup**: sets the initial height and width (based on the opened Console window), checks that the window isn't 
    too small, and initializes all windows.
- **\_init_main_window**: initializes the main window (sets the `self.window` attribute).
- **\_init_game_sub_windows**: initializes the following windows: game_area, side_menu, tips_area, logo_area, and game_status_area.
- **\_set_window_sizes**: sets sizes for all windows dynamically.
- **wait_for_keypress**: this method switches the main window to standby mode (uses blocking read, which will wait indefinitely for input).
- **is_user_press_key**: if we wait for a keypress without blocking read (not using **wait_for_keypress**), 
    the function 'curses.getch' returns '-1', which means that no key was pressed and `self.is_user_press_key(key)` returns False.
- **resize_menu_win_handler**: if the user resizes the window in any menu, this function draws a resizing message and 
    redraws the window using the new height and width.
- **resize_game_win_handler**: performs almost the same actions as **resize_menu_win_handler**, but in games, 
    using longer blocking intervals for optimization and re-setup of all windows.
- **handle_post_running_actions**: deletes all keys pressed by the user from memory (does not process them), and redraws the window.
- **redraw_window**: an empty function, aka abstract method, included as a reminder that this method should be 
    present in every inheritor class.

That's all. Avoid using underscores in front of method names outside of InterfaceManager, and all will be good.


### Achievements Manager

#### Base of Achievements Managers

The file './games_of_terminal/achievements_manager.py' contains the **AchievementsManager class**, 
which serves as the base class for all local achievement managers. It is responsible for unlocking achievements while 
the game is in progress. Most methods within this class are not intended for use outside of it, 
so it's best to leave it unchanged while it is functional.

- **set_all_achievements**: sets the following attributes:
    - `achievements_to_unlock`: an empty list that is filled with achievements that the user has unlocked. 
       All achievements in this list are awaiting unlocking and are not retained for a long time.
    - `achievements`: a list containing all locked achievements (only achievements locked in the current game).
    - `global_achievements`: a list containing all globally locked achievements.
- **get_locked_achievements**: returns a list of locked achievements in the current game or an empty list if the game is not in progress.
- **get_global_achievements**: returns a list of globally locked achievements.
- **get_begin_coordinates**: retrieves the height and width of the achievement frame and returns the beginning 
    coordinates (y, x) for the frame.
- **get_frame_height_and_width**: retrieves the achievement name length and calculates the height and width of the 
    achievement frame based on it. Returns the height and width of the achievement frame.
- **check**: the main method used outside of the AchievementsManager class. It populates the `achievements_to_unlock` 
    attribute, draws the achievements unlocking animation, updates achievement statuses in the database, 
    and redraws the main window. This method accepts the following keyword arguments:
    - `set_pause`: a boolean to enable pausing the game if achievements have been unlocked.
    - `**kwargs`: used for unique arguments passed to the local Achievement Manager and opened achievements that 
       cannot be unlocked automatically.
- **check_local_achievements**: checks all achievements in the `achievements` attribute for unlocking conditions and 
    populates the `achievements_to_unlock` attribute if the conditions return True.
- **check_global_achievements**: similar to the previous method (`check_local_achievements`), but for global achievements.
- **unlock_achievements**: unlocks all achievements from the `achievements_to_unlock` list in the database and 
    displays the unlocking animation.
- **handle_post_unlocking**: used after achievements have been unlocked. Resets the `achievements_to_unlock`, 
    `achievements`, and `global_achievements` attributes, redraws the window, and sets pause in the game if this option is enabled.
- **draw_achievement_unlocking_animation**: draws the full achievement unlocking animation.
- **draw_background**: draws the achievement background.
- **draw_achievement_unlocked_text**: draws the text indicating that an achievement has been unlocked.
- **draw_achievement_name**: draws the achievement name.
- **draw_frame_animation_chunk**: the current unlocking achievement animation assumes that the user watches how 
    the frame is drawn in two ways: from left to bottom and from bottom to left, with two dots. 
    This method draws two frame dots during the achievement unlocking animation.
- **draw_frame_animation**: draws the frame animation, appearing and disappearing, using the `draw_frame_animation_chunk` method.
- **has_achievement_been_unlocked**: this empty method, aka abstract method, is used in local achievement managers and 
    contains a 'match/case' construction that checks the received achievement for unlocking. 



#### Local Achievements Managers

In the description above, I outlined the base class for all local achievements managers, which cannot be used 
independently without additional functionality.

Here's how the achievement manager works in the example of the Snake game:

- First, navigate to `./games_of_terminal/games/snake/achievements_manager.py` to find the **SnakeGameAchievementsManager** class. 
  This serves as our local achievement manager. It requires one method: `has_achievement_been_unlocked`, 
  which receives an achievement and unique keyword arguments, checks the unlocking condition, and returns True if 
  the achievement can be unlocked or False otherwise. The local achievement manager can also include other methods 
  necessary for checking conditions for unlocking achievements. Take a look at the current implementations for more details.

- Next, in the *core.py* file of the Snake game, within the *setup_game_stats* method, I've added the following line: 
  `self.achievement_manager = SnakeGameAchievementsManager(self)`. This action initializes the current achievement manager 
  and waits for the use of the *check* method.

- So now, all you need to do is include the line `self.achievement_manager.check()` in your code to periodically check 
  for achievement unlocking during gameplay.



### Logger

File './games_of_terminal/log.py' contains Logger.


##
### Guide is in progress..
##
