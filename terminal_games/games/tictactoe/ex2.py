import curses

# Constants
import random

KEY_ESC = 27
X = "X"
O: str = "O"
EMPTY = " "

draw = "Draw!"
wins = " wins!"

CELL_WIDTH = 4
CELL_HEIGHT = 2

TOP = "+" + "-" * (CELL_WIDTH - 1) + "+"
BOTTOM = TOP
padding_size = (CELL_WIDTH - 2) // 2 if CELL_WIDTH % 2 == 0 else (CELL_WIDTH - 2) // 2 + 1
LEFT_WALL = "|" + " " * padding_size
RIGHT_WALL = " " * padding_size + "|" if CELL_WIDTH % 2 == 0 else " " * (padding_size - 1) + "|"

TOP_OFFSET = 1
LEFT_OFFSET = 0

# Game setup
grid = [[EMPTY for x in range(3)] for y in range(3)]
Xs_turn = bool(random.getrandbits(1))

# Curses setup
win = curses.initscr()
win.nodelay(True)  # makes getch non blocking
win.keypad(True)  # block keyboard signals (^C ...)

curses.curs_set(0)
curses.noecho()  # do not print the keyboard inputs
curses.mousemask(curses.ALL_MOUSE_EVENTS)  # enable mouse events

rows, cols = win.getmaxyx()
key = 0
mx, my = CELL_WIDTH * len(grid[0]), CELL_HEIGHT * len(grid)

while key != KEY_ESC and key != ord("q"):  # Esc to close
    win.addstr(0, 0, str(rows) + EMPTY + str(cols))
    if Xs_turn:
        win.addstr(0, 0, "X's turn")
    else:
        win.addstr(0, 0, "O's turn")

    rows, cols = win.getmaxyx()

    # catch keyboard inputs
    key = win.getch()

    # catch mouse inputs
    if key == curses.KEY_MOUSE:
        _, mx, my, _, _ = curses.getmouse()

    # draw grid
    for x, row in enumerate(grid):
        for y, element in enumerate(row):
            win.addstr(x * 2 + 0 + TOP_OFFSET, y * (len(TOP) - 1) + LEFT_OFFSET, TOP)
            win.addstr(x * 2 + 1 + TOP_OFFSET, y * (len(TOP) - 1) + LEFT_OFFSET, LEFT_WALL + str(element) + RIGHT_WALL)
            win.addstr(x * 2 + 2 + TOP_OFFSET, y * (len(TOP) - 1) + LEFT_OFFSET, BOTTOM)

    # click on grid
    if LEFT_OFFSET <= mx < LEFT_OFFSET + CELL_WIDTH * len(grid[0]) and TOP_OFFSET <= my < TOP_OFFSET + CELL_HEIGHT \
            * len(grid):
        cellY = (mx - LEFT_OFFSET) // CELL_WIDTH
        cellX = (my - TOP_OFFSET) // CELL_HEIGHT

        if grid[cellX][cellY] == EMPTY:
            if Xs_turn:
                grid[cellX][cellY] = X
            else:
                grid[cellX][cellY] = O
            Xs_turn = not Xs_turn

    # check if game is over
    winners_line = CELL_HEIGHT * len(grid[0]) + 1 + TOP_OFFSET

    if EMPTY not in grid[0] and EMPTY not in grid[1] and EMPTY not in grid[2]:
        win.addstr(winners_line, 0, draw)
    # check rows
    for row in grid:
        if row[0] == row[1] == row[2] and row[0] != EMPTY:
            win.addstr(winners_line, 0, f"{row[0]}" + wins)
            curses.mousemask(0)
            break

    # check columns
    for x in range(len(grid[0])):
        if grid[0][x] == grid[1][x] == grid[2][x] and grid[0][x] != EMPTY:
            win.addstr(winners_line, 0, f"{grid[0][x]}" + wins)
            curses.mousemask(0)
            break

    # check diagonals
    if grid[0][0] == grid[1][1] == grid[2][2] and grid[0][0] != EMPTY:
        win.addstr(winners_line, 0, f"{grid[0][0]}" + wins)
        curses.mousemask(0)

    if grid[0][2] == grid[1][1] == grid[2][0] and grid[0][2] != EMPTY:
        win.addstr(winners_line, 0, f"{grid[0][2]}" + wins)
        curses.mousemask(0)

    win.refresh()

curses.endwin()
