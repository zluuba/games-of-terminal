# Games Of Terminal
**Games Of Terminal** (or GOT) is a console-based gaming platform where classic games like 
Minesweeper, Tetris, Snake, and TicTacToe come to life in your terminal. 
With customization, achievements, and flexibility, GOT offers a diverse and enjoyable gaming experience 
in your favourite environment - **terminal**.

![got-cover](https://github.com/zluuba/games-of-terminal/assets/87614163/954898e1-c330-4798-82a4-d65558e377a8)
*picture was created by [leonardo.ai](https://leonardo.ai/)*


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

Install GOT package:
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
Navigate through the options using the ↓ and ↑ arrows (or WS keys).  
Press Enter to initiate the selected game.

Game Controls:
```ch
Arrows (↓ and ↑) or WS keys - control game

P - pause/unpause
R - restart
T - show/hide rules, tips, and settings
M - open/close side menu
```
To exit any window (menu, game, or settings), press Esc.  
**See demos [here](https://github.com/zluuba/games-of-terminal#demos).**


## Project Features

GOT has a lot of features, this is the full list of them:

1. **Achievements**: GOT has 40+ achievements, so you can [get them all](https://github.com/zluuba/games-of-terminal/tree/main/docs/achievements.md). Or you can't? ;)
2. **Customizing**: in every game, you have the option to choose a color scheme that suits your preferences, 
   create your own custom color scheme, or explore different game modes.
3. **Settings**: you can view your stats, customize your GOT experience by setting your username (yes, it matters), 
   adjust game preferences, and warm the author's heart by discovering a secret option.
4. **Autosave**: no matter if you overlook your game and simply exit, the game automatically saves your current progress 
   and asks the next time you want to continue an unfinished game. And, of course, GOT has pause and restart functions.
5. **Adaptability**: GOT adjusts to the user and automatically resizes the window when the user changes the size of the 
   terminal window. Regardless of whether you are in the menu, settings, or playing the game, 
   the interface can detect terminal resizing and redraw the window to create a better experience.
6. **Flexibility**: the side block with the logo, menu, and game status area has a fixed width but flexible height. 
   The game window has fully flexible parameters. In some games, it helps to add more game items (as in Minesweeper:
   the bigger the terminal window, the more game cells you will get), while in other games, it adjusts the size of the 
   elements (as in TicTacToe).
7. **Versatility**: whether you have a new MacBook or an old Asus (or a new Asus and an old MacBook), 
   GOT doesn't strain the processor, ensuring you the ability to play various games. I tested it on my affordable 
   2014 Asus, and it works perfectly. P.S. Yes, console apps can make the heart of your device stop beating too.
8. **Testing**: I utilized the curses library to interact with the terminal, and as curses operates at a low level, 
   simulating or mocking it in a controlled testing environment proves challenging. Consequently, GOT has tests for 
   non-terminal logic, and manual testing has played a significant role. If you encounter any issues or shortcomings, 
   please [report me about it](https://github.com/zluuba/games-of-terminal/tree/main/docs/issue-reporting-guide.md).
9. **Supporting**: I have a deep affection for this project and take care of it, ensuring continuous support and development. 
   If you share the same passion, you can [help me with that](https://github.com/zluuba/games-of-terminal/tree/main/docs/contributing-guide.md).


## For Developers

In this section, you'll find information about documentation, instructions for integrating your own games 
into GOT, details on how to contribute to the project, and bug reporting.

### Project Documentation
To delve into the technical details and explore documentation, head over to [Documentation](https://github.com/zluuba/games-of-terminal/tree/main/docs/developer-guide.md).

### Implementing Your Own Game
If you enjoy GOT, Python, and would like to create your own game with the GOT interface, 
be sure to read this detailed [instruction on game implementation](https://github.com/zluuba/games-of-terminal/tree/main/docs/creating-your-own-game.md).

### Contributing
If you've implemented your own game and would like to share it with others or have ideas to improve this project, 
I would be thrilled to welcome your contribution. 
For all the details, please visit [this page](https://github.com/zluuba/games-of-terminal/tree/main/docs/contributing-guide.md).

### Bug Reporting
If you encounter any issues, discover a bug while using GOT, 
or have any ideas to improve, please help me enhance the project by reporting it. 
Follow the steps outlined in the 
[issue reporting guide](https://github.com/zluuba/games-of-terminal/tree/main/docs/issue-reporting-guide.md) 
to create an issue.


## Upcoming Features

Here are some features I'm planning to implement in future releases:

### New Games:
- 2048 Game
- Sea Battle
- Sudoku
- Chess

### Game Features:
- Sea Battle with other humans using the Internet

Feel free to [suggest additional features](https://github.com/zluuba/games-of-terminal/tree/main/docs/issue-reporting-guide.md) 
or share your ideas!

## Demos

Demonstrations of the GOT interface and how to play the games.

*add GIFs or videos*


##

**Games Of Terminal | by [zluuba](https://github.com/zluuba)**
