# Games Of Terminal
Games Of Terminal (or GOT) is a console-based gaming platform where classic games like 
Minesweeper, Tetris, Snake, 2048, and TicTacToe come to life in your terminal. 
With customization, achievements, and flexibility, GOT offers a diverse and enjoyable gaming experience 
in your favourite environment - terminal.

*add a GIF showcasing the gameplay process.*


## Requirements

Make sure you have the following installed:

- [Python](https://www.python.org/), version 3.9 or higher. You can download it [here](https://www.python.org/downloads/).
- [Poetry](https://python-poetry.org/), version 1.2.0 or higher. Install it by following the instructions [here](https://python-poetry.org/docs/#installation).


## Installation

Open a terminal window.
Clone this repository or download it with pip:
```bash
git clone https://github.com/zluuba/games-of-terminal.git
```
```bash
pip install --user git+https://github.com/zluuba/games-of-terminal.git
```

Navigate to the downloaded directory and install dependencies:
```bash
cd games-of-terminal
make install
```

Install Games Of Terminal package:
```bash
make build
make package-install
```


## Usage

To start the games, use the following command:
```ch
got-games
```

Upon launching, you'll encounter the menu.  
Navigate through the options using the ↓ and ↑ arrows (or WASD).  
Press Enter to initiate the selected game.

Game Controls:
```ch
Arrows (↓ and ↑) or WASD - control game

P - pause/unpause
R - restart
T - show/hide rules, tips, and settings
M - open/close side menu
```
To exit any window (menu, game, or settings), press Esc.  
See demos [here](https://github.com/zluuba/games-of-terminal#demos).


## Project Specifics

GOT have some specifics, this is full list of it:

1. **Achievements**: GOT has 30+ achievements, so enjoy trying to [get them all](https://github.com/zluuba/games-of-terminal/tree/main/docs/achievements.md)!
2. **Customizing**: in every game, you can choose a color scheme that you like or create your own color scheme.
3. **Auto-resizing**: GOT automatically resizes the window when the user changes the size of the terminal window. Regardless 
   of whether you are in the menu, settings, or playing the game, the interface can detect terminal resizing and redraw the window.
4. **Flexibility**: the side block with the logo, menu, and game status area has a fixed width but flexible height. 
   The game window has fully flexible parameters. In some games, it helps to add more game items (as in Minesweeper:
   the bigger the terminal window, the more game cells you will get), while in other games, it adjusts the size of the 
   elements (as in TicTacToe).
5. **Settings**: you can customize your GOT experience by setting your username, game preferences, viewing your stats, and more.
6. **Care**: no matter if you overlook your game and simply exit, the game automatically saves your current progress 
   and asks the next time you want to continue an unfinished game. And, of course, GOT has pause and restart functions.
7. **Versatility**: no matter whether you have a new MacBook or an old Asus (or a new Asus and an old MacBook), GOT does 
   not strain the processor, ensuring that you have the ability to play various games. 
   I tested it on my affordable 2014 Asus, and it works perfectly.
8. **Testing**: I utilized the curses library to interact with the terminal, and as curses operates at a low level, 
   simulating or mocking it in a controlled testing environment proves challenging. Consequently, GOT has tests for 
   non-terminal logic, and manual testing has played a significant role. If you encounter any issues or shortcomings, 
   please [report me about it](https://github.com/zluuba/games-of-terminal/tree/main/docs/issue_reporting_guide.md).
9. **Supporting**: I have a deep affection for this project and take care of it, ensuring continuous support and development. 
   If you share the same passion and would like to contribute, you can [help me with that](https://github.com/zluuba/games-of-terminal/tree/main/docs/contributing_guide.md).


## For Developers

In this section, you'll find information about documentation, instructions for integrating your own games 
into Games Of Terminal (GOT), details on how to contribute to the project, and bug reporting.

### Project Documentation
To delve into the technical details and explore documentation, head over to [Documentation](https://github.com/zluuba/games-of-terminal/tree/main/docs/developer-guide.md).

### Implementing Your Own Game
If you enjoy GOT, Python, and would like to create your own game with the GOT interface, 
be sure to read this detailed [instruction on game implementation](https://github.com/zluuba/games-of-terminal/tree/main/docs/creating-your-own-game.md).

### Contributing
If you've implemented your own game and would like to share it with others or have ideas to improve this project, 
I would be thrilled to welcome your contribution. <br>
For all the details, please visit [this page](https://github.com/zluuba/games-of-terminal/tree/main/docs/contributing_guide.md).

### Bug Reporting
If you encounter any issues, discover a bug while using Games Of Terminal (GOT), 
or have any ideas to improve, please help me enhance the project by reporting it. 
Follow the steps outlined in the 
[issue reporting guide](https://github.com/zluuba/games-of-terminal/tree/main/docs/issue_reporting_guide.md) 
to create an issue.


## Upcoming Features

Here are some features I'm planning to implement in future releases:

### New Games:
- Sea Battle
- Sudoku
- Chess

### Game Features:
- Sea Battle with other humans using the Internet

Feel free to suggest additional features or share your ideas!

## Demos

Demonstrations of the GOT interface and how to play the games.

*add GIFs or videos*


##

**Games Of Terminal | by [zluuba](https://github.com/zluuba)**
