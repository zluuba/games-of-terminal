# Games Of Terminal

[![linter-check](https://github.com/zluuba/games-of-terminal/actions/workflows/linter-check.yml/badge.svg)](https://github.com/zluuba/games-of-terminal/actions/workflows/linter-check.yml)

**Games Of Terminal** (or GOT) is a console-based gaming platform where classic games like Minesweeper, Tetris, 
Snake, and TicTacToe come to life. With customization, achievements, and flexibility, 
GOT offers a diverse and enjoyable gaming experience in your favourite environment - **console**. 

 ![got-intro](https://github.com/zluuba/games-of-terminal/assets/87614163/58c985bd-38f8-4d6c-a4a0-73e1713df497)
*GIF with Games Of Terminal interaction demo (sped-up)*


## Requirements
This package has no dependencies, it was intentionally designed this way.  
So, you only need to have [Python](https://www.python.org/) installed (version 3.11 or higher). 
You can download it [here](https://www.python.org/downloads/).


## Installation

Open a terminal window.  
Clone this repository (with [Git](https://git-scm.com/downloads)) or download it with [Pip](https://pip.pypa.io/en/stable/installation/):
```bash
git clone https://github.com/zluuba/games-of-terminal.git
```
```bash
pip install --user git+https://github.com/zluuba/games-of-terminal.git
```

Navigate to the downloaded directory and install package:
```bash
cd games-of-terminal
make install
```


## Usage

To start the games, use the following command:
```ch
got-games
```

Upon launching, you'll encounter the menu. Here are some useful keys:
- Navigate through the options using the **↓ and ↑ arrows** (or WS keys).  
- Press **Enter** to initiate the selected item.  
- To exit any window (menu, game, or settings), press **Esc**.  
- To enter *Detail mode* in the Achievements or All Settings sections, press the **Spacebar**.  

Important note: to ensure the app functions correctly, you need to **keep your keyboard set to the English layout**.

**See demos [here](https://github.com/zluuba/games-of-terminal#demos).**


## Project Features

GOT has many advantages, this is the full list of them:

1. **Achievements**: GOT has 35+ achievements, so you can [get them all](https://github.com/zluuba/games-of-terminal/tree/main/docs/achievements.md). Or you can't? ;)
2. **Customizing**: in every game, you have the option to choose a color scheme that suits your preferences, 
   create your own custom color scheme (in development), or explore different game modes.
3. **Settings**: you can view your stats, customize your GOT experience by setting your username (yes, it matters), 
   adjust game preferences, and warm the author's heart by discovering a secret option.
4. **Autosave**: no matter if you overlook your game and simply exit, the game automatically saves your current progress 
   and asks the next time you want to continue an unfinished game (in development). 
   And, of course, GOT has pause and restart functions.
5. **God Mode**: You can add **your own game** to GOT. Yes. 
   Read [this documentation](https://github.com/zluuba/games-of-terminal/tree/main/docs/creating-your-own-game.md) and have fun!
6. **Adaptability**: GOT adjusts to the user and automatically resizes the window when the user changes the size of the 
   terminal window. Regardless of whether you are in the menu, settings, or playing the game, 
   the interface can detect terminal resizing and redraw the window to create a better experience.
7. **Flexibility**: the side block with the logo, menu, and game status area has a fixed width but flexible height. 
   The game window has fully flexible parameters. In some games, it helps to add more game items (as in Minesweeper:
   the bigger the terminal window, the more game cells you will get), while in other games, it adjusts the size of the 
   elements (as in TicTacToe).
8. **Versatility**: whether you have a new MacBook or an old Asus (or a new Asus and an old MacBook), 
   GOT doesn't strain the processor (maybe just a little), ensuring you the ability to play various games. 
   I tested it on different VMs (MacOS and Ubuntu), and it works perfectly. P.S. I tried testing it on Windows, 
   but it consistently crashes during installation in my virtual machine app, so I've concluded that PC gaming already 
   offers enough games, so if GOT doesn't work on Windows (and I'm sure it works perfectly too), I don't mind.
9. **Testing**: I utilized the Curses library to interact with the terminal, and as Curses operates at a low level, 
   simulating or mocking it in a controlled testing environment proves challenging. Consequently, GOT has tests for 
   non-terminal logic, and manual testing has played a significant role. If you encounter any issues or shortcomings, 
   please [report me about it](https://github.com/zluuba/games-of-terminal/tree/main/docs/issue-reporting-guide.md).
10. **Supporting**: With a deep affection for this project, I am committed to its continuous support and development. 
   If you share the same passion, you can [help me with that](https://github.com/zluuba/games-of-terminal/tree/main/docs/contributing-guide.md). Thank you!


## For Developers

In this section, you'll find information about documentation, instructions for integrating your own games 
into GOT, details on how to contribute to the project, and bug reporting.

### Project Documentation
For technical details and project documentation, visit [Documentation](https://github.com/zluuba/games-of-terminal/tree/main/docs/developer-guide.md).

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

### F.A.Q.
[Here are some answers](https://github.com/zluuba/games-of-terminal/tree/main/docs/frequently-asked-questions.md) about this project.

### Upcoming Features
I have a lot of ideas (and bugs), so [here is a list](https://github.com/zluuba/games-of-terminal/tree/main/docs/upcoming-features.md) of them.
  
  
**Feel free to [suggest additional features](https://github.com/zluuba/games-of-terminal/tree/main/docs/issue-reporting-guide.md) 
or share your ideas!**


## Demo
Games Of Terminal interaction demo (sped-up).

https://github.com/zluuba/games-of-terminal/assets/87614163/a661f605-de07-4941-bf93-bbcd4dfe3fa6



##

**Games Of Terminal | by [zluuba](https://github.com/zluuba)**
