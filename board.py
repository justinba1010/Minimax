import copy, gc
ALLPIECES = {-6:0x265A,-5:0x265B,-4:0x265C,-3:0x265D,-2:0x265E,-1:0x265F,0:0xa0,1:0x2659,2:0x2658,3:0x2657,4:0x2656,5:0x2655,6:0x2654}
PIECES = ["EMPTY","PAWN","KNIGHT","BISHOP","ROOK","QUEEN","KING"]
SCORES = {-6:-100,-5:-9,-4:-5,-3:-3,-2:-3,-1:-1,0:0,1:1,2:3,3:3,4:5,5:9,6:100}
ROWS = 8
COLUMNS = 8
WHITEPAWNDOUBLES = [[2,0]]
BLACKPAWNDOUBLES = [[-2,0]]
WHITEPAWNENPASSANT = [[1,1],[1,-1]]
BLACKPAWNENPASSANT = [[-1,1],[-1,-1]]
WHITEPAWNNORMAL = [[1,0]]
BLACKPAWNNORMAL = [[-1,0]]
WHITE = 1
BLACK = -1
KNIGHTMOVES = [[2,-1],[2,1],[-2,1],[-2,-1],[1,2],[1,-2],[-1,2],[-1,-2]]
BISHOPVECTORS = [[1,1],[1,-1],[-1,1],[-1,-1]]
KINGMOVES = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
ROOKVECTORS = [[1,0],[-1,0],[0,1],[0,-1]]
PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6
class BaseBoard():
    def __init__(self, board = None, turn = 1):
        if board == None:
            self.board = [[0 for b in range(0,COLUMNS)] for i in range(0,ROWS)]
            self.board[0] = [4,2,3,5,6,3,2,4]
            self.board[1] = [1,1,1,1,1,1,1,1]
            self.board[6] = [-1,-1,-1,-1,-1,-1,-1,-1]
            self.board[7] = [-4,-2,-3,-5,-6,-3,-2,-4]

        else: self.board = board
        self.enpassant = False
        self.enpassantcolumn = None
        self.whitecastlekingside = True
        self.whitecastlequeenside = True
        self.blackcastlekingside = True
        self.blackcastlequeenside = True
        self.turn = turn
        self.over = False
    def winner(self):
        score = 0
        #Simple Count Pieces
        for x in range(0,8):
            for y in range(0,8):
                score += SCORES[self.board[x][y]]
        #Add possible moves
        #score += self.turn*len(self.genlegalmoves(self.turn))*0.1
        return score
    def isover(self):
        if self.over:
            return self.winner()/abs(self.winner())
    def nowover(self):
        self.over = True
    def legalmove(self,move, turn = None):
        turn = self.turn if turn == None else turn
        piece1 = self.pieceat(move.row, move.column)
        color1 = self.colorat(move.row, move.column)
        piece2 = self.pieceat(move.newrow, move.newcolumn)
        color2 = self.colorat(move.newrow, move.newcolumn)
        
        #First check to see if it is the correct player making the move
        if turn != color1:
            return False
        #Check to see if move lands on board
        if move.onboard() == False:
            return False
        #Make sure they aren't taking the same piece
        if color1 == color2:
            return False
        #PAWN MOVES
        if piece1 == PAWN:
            #Enpassant
            if self.enpassant == True:
                if turn == WHITE:
                    if move.move in WHITEPAWNENPASSANT and move.newcolumn == self.enpassantcolumn and move.row == 4:
                        return True
                if turn == BLACK:
                    if move.move in BLACKPAWNENPASSANT and move.newcolumn == self.enpassantcolumn and move.row == 3:
                        return True
            #OverTake
            if turn == WHITE:
                if color2 != 0 and color2 != color1:
                    if move.move in WHITEPAWNENPASSANT:
                        return True
            if turn == BLACK:
                if color2 != 0 and color2 != color1:
                    if move.move in BLACKPAWNENPASSANT:
                        return True
            if color2 != 0:
                return False
            #Doubles
            if turn == WHITE:
                if move.row == 1:
                    if move.move in WHITEPAWNDOUBLES:
                        return True
            if turn == BLACK:
                if move.row == 6:
                    if move.move in BLACKPAWNDOUBLES:
                        return True

            #Single
            if turn == WHITE:
                if move.move in WHITEPAWNNORMAL:
                    return True
            if turn == BLACK:
                if move.move in BLACKPAWNNORMAL:
                    return True
            return False
        #KNIGHT MOVES
        if piece1 == KNIGHT:
            if move.move in KNIGHTMOVES:
                return True
        #BISHOP MOVES
        if piece1 == BISHOP:
            if move.vector in BISHOPVECTORS:
                if move.diagonal == False: return False
                for obstacle in move.inbetween():
                    if self.colorat(obstacle[0],obstacle[1]) != 0:
                        return False
                return True
        #ROOK MOVES
        if piece1 == ROOK:
            if move.vector in ROOKVECTORS:
                for obstacle in move.inbetween():
                    if self.colorat(obstacle[0],obstacle[1]) != 0:
                        return False
                return True
        #QUEEN MOVES
        if piece1 == QUEEN:
            if move.vector in BISHOPVECTORS:
                if move.diagonal == False: return False
                for obstacle in move.inbetween():
                    if self.colorat(obstacle[0],obstacle[1]) != 0:
                        return False
                return True
            if move.vector in ROOKVECTORS:
                for obstacle in move.inbetween():
                    if self.colorat(obstacle[0],obstacle[1]) != 0:
                        return False
                return True
        #KING MOVES
        if piece1 == KING:
            if move.move in KINGMOVES:
                return True
        #CASTLE MOVES
        if piece1 == KING:
            castle = False
            if color1 == WHITE:
                if move.newrow == 0:
                    if move.newcolumn == 2:
                        castle = (self.board[0][0] == ROOK * WHITE)
                        castle &= (self.board[0][4] == KING * WHITE)
                        castle &= (self.board[0][1] == 0)
                        castle &= (self.board[0][2] == 0)
                        castle &= (self.board[0][3] == 0)
                        castle &= self.whitecastlequeenside
                    if move.newcolumn == 6:
                        castle = (self.board[0][7] == ROOK * WHITE)
                        castle &= (self.board[0][4] == KING * WHITE)
                        castle &= (self.board[0][5] == 0)
                        castle &= (self.board[0][6] == 0)
                        castle &= self.whitecastlekingside
            if color1 == BLACK:
                if move.newrow == 7:
                    if move.newcolumn == 2:
                        castle = (self.board[7][0] == ROOK * BLACK)
                        castle &= (self.board[7][4] == KING * BLACK)
                        castle &= (self.board[7][1] == 0)
                        castle &= (self.board[7][2] == 0)
                        castle &= (self.board[7][3] == 0)
                        castle &= self.blackcastlequeenside
                    if move.newcolumn == 6:
                        castle = (self.board[7][7] == ROOK * BLACK)
                        castle &= (self.board[7][4] == KING * BLACK)
                        castle &= (self.board[7][5] == 0)
                        castle &= (self.board[7][6] == 0)
                        castle &= self.blackcastlekingside
            return castle
        return False
    def colorat(self,row,column):
        color = 0 if self.board[row][column] == 0 else 1 if self.board[row][column] > 0 else -1
        return color
    def pieceat(self,row,column):
        return abs(self.board[row][column])
    def makemove(self,move,turn=None):
        turn = self.turn if turn == None else turn
        piece1 = self.pieceat(move.row, move.column)
        color1 = self.colorat(move.row, move.column)
        piece2 = self.pieceat(move.newrow, move.newcolumn)
        color2 = self.colorat(move.newrow, move.newcolumn)
        #Check if legal
        if self.legalmove(move,turn):
            if piece2 == KING:
                self.nowover()
            #Enpassants
            if self.enpassant and (((move.row == 4 and color1 == WHITE) or (move.row == 3 and color1 == BLACK))) and piece1 == PAWN:
                if self.enpassantcolumn == move.newcolumn:
                    self.board[move.newrow][move.newcolumn] = self.board[move.row][move.column]
                    self.board[move.row][move.column] = 0
                    self.board[move.row][move.newcolumn] = 0
                    self.enpassant = False
                    self.enpassantcolumn = None
                    self.turn *= -1
                    return True
            if piece1 == PAWN and (move.move in WHITEPAWNDOUBLES or move.move in BLACKPAWNDOUBLES):
                self.enpassant = True
                self.enpassantcolumn = move.column
                self.board[move.newrow][move.newcolumn] = self.board[move.row][move.column]
                self.board[move.row][move.column] = 0
                self.turn *= -1
                return True
            if piece1 == PAWN and (move.move in WHITEPAWNNORMAL or move.move in BLACKPAWNNORMAL):
                if color2 != 0:
                    return False
                if color1 == WHITE:
                    if move.newrow == 7:
                        self.board[move.row][move.column] = 0
                        self.board[move.newrow][move.newcolumn] = QUEEN * WHITE
                        self.turn *= -1
                        return True
                if color1 == BLACK:
                    if move.newrow == 0:
                        self.board[move.row][move.column] = 0
                        self.board[move.newrow][move.newcolumn] = QUEEN * BLACK
                        self.turn *= -1
                        return True
            self.enpassantcolumn = None
            self.enpassant = True
            
            #CASTLE
            if piece1 == KING:
                if color1 == WHITE:
                    self.whitecastlekingside = False
                    self.whitecastlequeenside = False
                if color1 == BLACK:
                    self.blackcastlekingside = False
                    self.blackcastlequeenside = False
                if move.move in KINGMOVES:
                    self.board[move.newrow][move.newcolumn] = self.board[move.row][move.column]
                    self.board[move.row][move.column] = 0
                    self.turn *= -1
                    return True
                #CASTLES
                if color1 == WHITE:
                    if move.newrow == 0:
                        if move.newcolumn == 2:
                            self.board[0][0] = 0
                            self.board[0][1] = 0
                            self.board[0][2] = KING * WHITE
                            self.board[0][3] = ROOK * WHITE
                            self.board[0][4] = 0
                        if move.newcolumn == 6:
                            self.board[0][4] = 0
                            self.board[0][5] = ROOK * WHITE
                            self.board[0][6] = KING * WHITE
                            self.board[0][7] = 0
                if color1 == BLACK:
                    if move.newrow == 7:
                        if move.newcolumn == 2:
                            self.board[7][0] = 0
                            self.board[7][1] = 0
                            self.board[7][2] = KING * BLACK
                            self.board[7][3] = ROOK * BLACK
                            self.board[7][4] = 0
                        if move.newcolumn == 6:
                            self.board[7][4] = 0
                            self.board[7][5] = ROOK * BLACK
                            self.board[7][6] = KING * BLACK
                            self.board[7][7] = 0
                self.turn *= -1
                return True
            #Cancel Possible Castles
            if piece1 == ROOK:
                if color1 == WHITE:
                    if move.column == 0:
                        self.whitecastlequeenside = False
                    elif move.column == 7:
                        self.whitecastlekingside = False
                elif color1 == BLACK:
                    if move.column == 0:
                        self.blackcastlequeenside = False
                    if move.column == 7:
                        self.blackcastlekingside = False
            if color1 == WHITE and piece1 == KING:
                self.whitecastlekingside = False
                self.whitecastlequeenside = False
            if color1 == BLACK and piece1 == KING:
                self.blackcastlekingside = False
                self.blackcastlequeenside = False
            self.board[move.newrow][move.newcolumn] = self.board[move.row][move.column]
            self.board[move.row][move.column] = 0
            self.turn *= -1
            return True
        return False
    def genlegalmoves(self,player):
        pieces = self.genpiecelocations(player)
        moves = []
        for piece in pieces:
            moves += self.genmovespiece(piece,player)
        return moves
    def genpiecelocations(self,player):
        pieces = []
        for x in range(0,8):
            for y in range(0,8):
                pieces.append([x,y])
        return pieces
    def genmovespiece(self,piece,player):
        moves = []
        for x in range(0,8):
            for y in range(0,8):
                move = Move(piece[0],piece[1],x,y)
                if self.legalmove(move,):
                    moves.append(move)
        return moves
    def __unicode__(self):
        pboard = " |0|1|2|3|4|5|6|7|"
        for x in range(0,8):
            pboard += unichr(0x000A)+str(x).encode()+"|"
            for y in range(0,8):
                pboard += unichr(ALLPIECES[self.board[x][y]])+"|"
        return pboard


class Move():
    def __init__(self, row, column, newrow, newcolumn):
        self.row = row
        self.column = column
        self.newrow = newrow
        self.newcolumn = newcolumn
        self.vector = [(self.newrow-self.row)/max(1,abs(self.newrow-self.row)),(self.newcolumn-self.column)/max(1,abs(self.newcolumn-self.column))]
        self.move = [(self.newrow-self.row),(self.newcolumn-self.column)]
        self.diagonal = abs(self.move[0]) == abs(self.move[1])
    def onboard(self):
        if self.row < 0 or self.row >= 8:
            return False
        if self.newrow < 0 or self.newrow >= 8:
            return False
        if self.column < 0 or self.column >= 8:
            return False
        if self.newcolumn < 0 or self.newcolumn >= 8:
            return False
        return True
    def inbetween(self):
        blocks = []
        x = self.row
        y = self.column
        z = 0
        if self.vector[0] != 0 and self.vector[1] != 0:
            if self.diagonal == False: return blocks
        while (x != self.newrow or y != self.newcolumn) and z < 10:
            x += self.vector[0]
            y += self.vector[1]
            blocks.append([x,y])
            z += 1
        return blocks[:-1]
    def __str__(self):
        return ("%s|%s to %s|%s" % (self.row,self.column,self.newrow,self.newcolumn))
    def __eq__(self, other):
        if other is None:
            return False
        return self.row == other.row and self.column == other.column and self.newrow == other.newrow and self.newcolumn == other.newcolumn
    def __ne__(self, other):
        return not self.__eq__(other)