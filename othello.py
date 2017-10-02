#To run rename this to board.py and rename board.py to chess.py

X = 1
O = -1
COLUMNS = 6
ROWS = 6

VECTORS = [[1,1],[-1,-1],[1,0],[0,1],[0,-1],[-1,0],[1,-1],[-1,1]]

class BaseBoard():
    def __init__(self, board = None, turn = 1):
        if board == None:
            self.board = [[0 for b in range(0,COLUMNS)] for i in range(0,ROWS)]
            #Set the beginning set up of the board
            self.board[ROWS//2-1][COLUMNS//2-1] = 1
            self.board[ROWS//2][COLUMNS//2] = 1
            self.board[ROWS//2][COLUMNS//2-1] = -1
            self.board[ROWS//2-1][COLUMNS//2] = -1
        else: self.board = board
        self.turn = turn
        self.over = False
    def winner(self):
        #Calculate the score of the game as minimally as possible
        z = 0
        for x in range(0,ROWS):
            for y in range(0,COLUMNS):
                z += self.board[x][y]
        return z
    def isover(self):
        #Let's AI know if the game is over
        if len(self.genlegalmoves(self.turn)) == 0: self.over = True
    def legalmove(self,moveblock, turn = None):
        #Let's AI know if a certain move <object> is a legal move
        if turn == None: turn = self.turn
        legal = False
        blocks = []
        if self.whoisat(moveblock) != 0: return False
        turn = turn
        for vector in VECTORS:
            currentblock = moveblock
            tempblocks = []
            end = False
            while currentblock.returniflegal() != None and not end:
                currentblock = (currentblock + vector).returniflegal()
                if currentblock == None:
                    end = True
                    break
                end = True #Only keep going if the next block is the opponent
                if self.whoisat(currentblock) == turn *-1:
                    tempblocks.append(currentblock)
                    end = False
                elif self.whoisat(currentblock) == turn:
                    for block in tempblocks:
                        blocks.append(block)
                    end = True
        if len(blocks) == 0:
            return False
        else: return blocks
    def whoisat(self,block):
        #Grid based games, let's AI know which player is at position
        if block.returniflegal() == None:
            return None
        return self.board[block.row][block.column]
    def makemove(self,moveblock,turn=None):
        #Changes board space
        if turn == None: turn = self.turn
        if not self.legalmove(moveblock,turn):
            return
        blocks = self.legalmove(moveblock,turn)
        blocks.append(moveblock)
        for block in blocks:
            self.board[block.row][block.column] = turn
        self.turn *= -1
        self.isover()
    def genlegalmoves(self,player):
        #Gives AI list of all possible moves
        #Brute force or heuristic, but needs all and only legal moves to work correctly.
        legalmoves = []
        for row in range(0,ROWS):
            for column in range(0,COLUMNS):
                if self.legalmove(Move(row,column), player) is not False:
                    legalmoves.append(Move(row,column))
        return legalmoves
    def __unicode__(self):
        #Display board in text version
        pboard = " "
        for row in range(0,ROWS): pboard += "|" + str(row)
        pboard += "\n"
        for row in range(0,ROWS):
            pboard += str(row) + "|"
            for column in range(0,COLUMNS):
                pboard += "X" if self.board[row][column] == 1 else "O" if self.board[row][column] == -1 else "-" #X O or blank
                pboard += "|" if column != COLUMNS-1 else ""
            pboard += "\n" if row != ROWS-1 else ""

        return pboard

    def __str__(self):
        #For easy concatenation and such
        return self.__unicode__()


#Move Object
class Move():
    def __init__(self,row,column):
        self.row = row
        self.column = column
    def neighbors(self):
        neighbors = []
        for vector in VECTORS:
            neighbor = (self+vector).returniflegal()
            if neighbor != None: neighbors.append(neighbor)
        return neighbors
    def __add__(self,other):
            return Move(self.row+other[0],self.column+other[1])
    def returniflegal(self):
        if self.row < ROWS and self.column < COLUMNS and self.row >= 0 and self.column >= 0:
            return self
        return None
    def __str__(self):
        return ("%s|%s" % (self.row,self.column))
    def __eq__(self, other):
        if other is None:
            return False
        return self.row == other.row and self.column == other.column
    def __ne__(self, other):
        return not self.__eq__(other)
