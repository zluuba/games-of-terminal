import curses
import sys


class ticTacToe:
    """All the data of the current game"""

    def __init__(self, stdWindow, boardHeight=3, boardWidth=3, winCondition=3, overwriteable=True):
        # store grid size data
        self.boardHeight = int(boardHeight)
        self.boardWidth = int(boardWidth)
        self.winCondition = int(winCondition)
        self.overwriteable = bool(overwriteable)
        # 1. Draw up game windows
        # find out what "screen resolution" we have, from the std-window that's passed to object initiation
        maxYX = stdWindow.getmaxyx()

        # initiate the status window straight away - we use it for error messages
        self.statusWindow = curses.newwin(3, maxYX[1] - 10, maxYX[0] - 4, 5)

        # check if the game grid fits on the screen (TODO: make more better check)
        if boardHeight * 2 + 1 > maxYX[0] - 10:
            self.boardHeight = ((maxYX[0] - 10) / 2) - 1
            self.putStatus("The board was too high to fit on your screen and has been adjusted to " + str(boardHeight),
                           True)
            if self.winCondition > boardHeight:
                self.winCondition = boardHeight
        if boardWidth * 2 + 1 > (maxYX[1] / 2) - 10:
            self.boardWidth = (((maxYX[1] / 2) - 10) / 2) - 1
            self.putStatus("The board was too wide to fit on your screen and has been adjusted to " + str(boardWidth),
                           True)
            if self.winCondition > boardWidth:
                self.winCondition = boardWidth

        # translate the game grid size into appropriate window sizes
        # *2+1 gives space for a grid around each spot
        boardWinHeight = self.boardHeight * 2 + 1
        boardWinWidth = self.boardWidth * 2 + 1

        # set the info window height to 10 or game window height, whichever is bigger
        if boardWinHeight < 10:
            infoWinHeight = 10
        else:
            infoWinHeight = boardWinHeight
        # we'll be using (at least) one text window, and that should be roughly 1/4 of the screen
        textWidth = (maxYX[1] / 4)
        # define starting point of the game window. We'll place it roughly in the middle of the screen.
        begin_x = (maxYX[1] / 2 - boardWinWidth / 2)
        if begin_x < 0:
            begin_x = 0
        begin_y = (maxYX[0] / 2 - boardWinHeight / 2)
        if begin_y < 0:
            begin_y = 0
        # initiate curses windows
        # for visual nicety, all windows will have the same height
        self.gameWindow = curses.newwin(boardWinHeight, boardWinWidth, begin_y, begin_x)
        self.infoWindow = curses.newwin(infoWinHeight, textWidth, begin_y, (maxYX[1] - textWidth - 5))
        self.scoreWindow = curses.newwin(boardWinHeight, textWidth, begin_y, 5)

        # initiate game variables
        # define game control buttons
        # we use tuples, so that we may use several parallell setups
        # TODO: not sure about arrow codes here. The ABCD are hacks,
        # and should be replaced with some sort of curses.KEY_ values
        # the curses.KEY_UP etc doesn't seem to be working on my terminal.
        self.upKeys = ('k', 'w', 'A', curses.KEY_UP)
        self.downKeys = ('j', 's', 'B', curses.KEY_DOWN)
        self.leftKeys = ('h', 'a', 'D', curses.KEY_LEFT)
        self.rightKeys = ('l', 'd', 'C', curses.KEY_RIGHT)
        self.markKeys = (' ', '\n')
        self.quitKeys = ('Q', 'X', '\x04')
        self.winCond = winCondition
        # initiate the turn variable
        self.activePlayer = ""

        # draw up the status window. It'll currently state whose turn it is
        self.statusWindow.insstr(2, 1, 'Player turn: ' + self.activePlayer)
        self.statusWindow.border()

        # Draw up the game's visual grid
        # draw up horisonatl & vertical lines every 2 spaces
        self.gameWindow.border()
        for y in range(0, boardWinHeight):
            for x in range(0, boardWinWidth):
                if y == 0:
                    if x % 2 == 0:
                        self.gameWindow.addch(y, x, curses.ACS_TTEE, curses.A_DIM)
                    else:
                        self.gameWindow.addch(y, x, curses.ACS_HLINE, curses.A_DIM)
                elif x == 0:
                    if y % 2 == 0:
                        self.gameWindow.addch(y, x, curses.ACS_LTEE, curses.A_DIM)
                    else:
                        self.gameWindow.addch(y, x, curses.ACS_VLINE, curses.A_DIM)
                elif y == boardWinHeight - 1:
                    if x < boardWinWidth - 1:
                        if x % 2 == 0:
                            self.gameWindow.addch(y, x, curses.ACS_BTEE, curses.A_DIM)
                        else:
                            self.gameWindow.addch(y, x, curses.ACS_HLINE, curses.A_DIM)
                elif x == boardWinWidth - 1:
                    if y % 2 == 0:
                        self.gameWindow.addch(y, x, curses.ACS_RTEE, curses.A_DIM)
                    else:
                        self.gameWindow.addch(y, x, curses.ACS_VLINE, curses.A_DIM)
                else:
                    if y % 2 == 0 and x % 2 == 1:
                        self.gameWindow.addch(y, x, curses.ACS_HLINE, curses.A_DIM)
                    elif y % 2 == 1 and x % 2 == 0:
                        self.gameWindow.addch(y, x, curses.ACS_VLINE, curses.A_DIM)
                    elif y % 2 == 0 and x % 2 == 0:
                        self.gameWindow.addch(y, x, curses.ACS_PLUS, curses.A_DIM)
        self.gameWindow.addch(0, 0, curses.ACS_ULCORNER, curses.A_DIM)
        self.gameWindow.addch(0, boardWinWidth - 1, curses.ACS_URCORNER, curses.A_DIM)
        self.gameWindow.addch(boardWinHeight - 1, 0, curses.ACS_LLCORNER, curses.A_DIM)
        # curses hangs if we try to write to the bottom-right corner of a window...
        # but there seems to be a hack
        try:
            self.gameWindow.addch(boardWinHeight - 1, boardWinWidth - 1, curses.ACS_LRCORNER, curses.A_DIM)
        except:
            pass
        # self.gameWindow.border()

        # for i in range(0,boardWinHeight,2):
        # self.gameWindow.hline(i,1,hSgn,boardWinWidth)
        # for i in range(0,boardWinWidth,2):
        # self.gameWindow.vline(1,i,vSgn,boardWinHeight)
        # self.gameWindow.border()
        # get the size of the info window
        maxYX = list(self.infoWindow.getmaxyx())
        # increment for border
        maxYX[0] -= 2
        # printing will start inside the left border, so
        # increment for right border
        maxYX[1] -= 1
        # set info cursor position
        posit = [1, 1]
        # list of basic game info for the user
        infoStr = "Use w,s,a,d or j,k,h,l to move"
        infoStr += "\nor just arrow-keys"
        infoStr += "\nPress space or enter to put marker"
        infoStr += "\nType " + str(self.quitKeys) + " to quit"
        if self.overwriteable == True:
            infoStr += "\nBoard markers may be overwritten"
        else:
            infoStr += "\nBoard markers may not be overwritten"
        infoStr += "\n\n" + str(self.winCondition) + " in a row to win"
        # print the list in the info window
        for line in infoStr.split('\n'):
            if posit[0] <= maxYX[0]:
                self.infoWindow.addnstr(posit[0], posit[1], line, maxYX[1], curses.A_DIM)
                posit[0] += 1
                # if the current line was longer than the text window
                # split it and continue on the next line(s)
                while len(line) >= maxYX[1]:
                    line = line[maxYX[1] - 1:]
                    self.infoWindow.addnstr(posit[0], posit[1], line, maxYX[1], curses.A_DIM)
                    posit[0] += 1
        self.infoWindow.border()

        # initiate the game board grid, that will keep track of who's marked what spot
        # to get new instances of all objects in the grid, I think we have to use append()
        self.board = []
        for y in range(0, self.boardHeight):
            self.board.append([])
            for x in range(0, boardWidth):
                self.board[y].append(str())

        # initiate the status window text
        # self.statusWindow.insstr(1,1,"Player turn: ")
        self.putStatus()

        # run the togglePlayer function to initiate player turn
        self.togglePlayer()
        # set an empty winner variable
        self.winner = ""

        # initiate cursor position
        self.cursor = [0, 0]

        # refresh all windows (prints all windows to screen)
        self.infoWindow.refresh()
        self.scoreWindow.refresh()
        self.statusWindow.refresh()
        self.gameWindow.refresh()

        # move the cursor to the correct position
        self.gameWindow.move((1 + self.cursor[0] * 2), (1 + self.cursor[1] * 2))

    # definition to update the status window
    # if no text is supplied, updates to default "Player turn: [X0] state
    def putStatus(self, newText="Player turn: ", promptWait=False):
        if newText == "Player turn: ":
            newText += self.activePlayer
        self.statusWindow.clear()
        self.statusWindow.insstr(1, 1, newText)
        self.statusWindow.border()
        self.statusWindow.refresh()
        if promptWait == True:
            self.statusWindow.getkey()

    # function that marks a spot for a player
    def putMarker(self):
        # TODO: add functionality to allow/disallow overwrites
        # mark current position in the grid variable

        if self.overwriteable == True or self.board[self.cursor[0]][self.cursor[1]] == "":
            self.board[self.cursor[0]][self.cursor[1]] = str(self.activePlayer)

            # print the game grid
            for y in range(0, self.boardHeight):
                for x in range(0, self.boardWidth):
                    # on each position, print the character stored in the board variable
                    self.gameWindow.addstr((1 + y * 2), (1 + x * 2), str(self.board[y][x]))
            # print to screen
            self.gameWindow.refresh()

            # now that we've put a new marker, check if anyone's won
            self.checkWin()
            # and if not, switch player turn
            self.togglePlayer()
        else:
            self.putStatus('That position seems to be taken', True)
            self.putStatus()

    # function to toggle player, and anything else that should be done at the same time
    def togglePlayer(self):
        if self.activePlayer == 'X':
            self.activePlayer = '0'
        else:
            self.activePlayer = 'X'

        # type out the active player in the right spot in the status window
        # self.statusWindow.addch(1,14,self.activePlayer)
        # self.statusWindow.refresh()
        self.putStatus()

    def checkWin(self):

        # to check if anyone's won, we'll go through the game board position by position
        # and from each position, we'll start searching for rows of the same character

        # start with two nested loops to cover every position
        for y in range(0, self.boardHeight):
            for x in range(0, self.boardWidth):

                # z is the in-a-row counter
                # the searching variable is here because I hate 'break's in a loop
                z = 1
                searching = True
                # check horizontally, and exit if we hit a border
                while searching and (x + z) < self.boardWidth:
                    # if we're still on the same player/letter, increment
                    if self.board[y][x] == self.board[y][x + z]:
                        z += 1
                    # if not, exit
                    else:
                        searching = False
                    # if we've reached win conditions, set a winner
                    if z == self.winCondition:
                        self.winner = self.board[y][x]

                # check vertically, unless we found a winner in the last step
                z = 1
                searching = True
                while searching and (y + z) < self.boardHeight and self.winner == "":
                    if self.board[y][x] == self.board[y + z][x]:
                        z += 1
                    else:
                        searching = False
                    if z == self.winCondition:
                        self.winner = self.board[y][x]

                # check diagonally/right. exit if we hit any borders.
                z = 1
                searching = True
                while searching and (x + z) < self.boardWidth and (y + z) < self.boardHeight and self.winner == "":
                    if self.board[y][x] == self.board[y + z][x + z]:
                        z += 1
                    else:
                        searching = False
                    if z == self.winCondition:
                        self.winner = self.board[y][x]

                # check diagonally/left. exit if we hit any borders.
                z = 1
                searching = True
                while searching and (x - z) >= 0 and (y + z) < self.boardHeight and self.winner == "":
                    if self.board[y][x] == self.board[y + z][x - z]:
                        z += 1
                    else:
                        searching = False
                    if z == self.winCondition:
                        self.winner = self.board[y][x]

                # if we have a winner, print it!
                # TODO: the scoreWinner window is for "best-of-three" versions of the game. implement.
                if self.winner != "":
                    self.scoreWindow.insstr(self.winner + ' WINS!!!', curses.A_BLINK)
                    self.scoreWindow.getkey()
                    sys.exit(0)

    # function that interprets keypresses and takes appropriate action
    def readKey(self, keyPress):
        # interpret the four arrow keys, and move cursor (unless we're at the game edge)
        if keyPress in self.leftKeys:
            if self.cursor[1] > 0:
                self.cursor[1] -= 1
        elif keyPress in self.downKeys:
            if self.cursor[0] < self.boardHeight - 1:
                self.cursor[0] += 1
        elif keyPress in self.upKeys:
            if self.cursor[0] > 0:
                self.cursor[0] -= 1
        elif keyPress in self.rightKeys:
            if self.cursor[1] < self.boardWidth - 1:
                self.cursor[1] += 1

        # interpret quit keys, and exit
        elif keyPress in self.quitKeys:
            sys.exit(0)

        # interpret mark commands
        elif keyPress in self.markKeys:
            self.putMarker()

        # once we're done interpreting, move the cursor to appropriate position & update window
        # (this should be the last thing that happends before the game waits for player response
        # so it's important that we position the cursor here. Anything prior to here might be interfered with)
        self.gameWindow.move((1 + self.cursor[0] * 2), (1 + self.cursor[1] * 2))
        self.gameWindow.refresh()

    # function that captures keypresses
    # basically, this only points to the correct window
    def getkey(self):
        return self.gameWindow.getkey()
