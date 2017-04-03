import copy
import board
import random



class Node():
    def __init__(self, board = board.BaseBoard(), lastmove = 0):
        self.board = board
        self.value = self.board.winner()
        self.children = []
        self.turn = self.board.turn
        self.lastmove = lastmove
        self.bestmove = None
    def generate(self,branches):
        if branches <= 0:
            return
        #Make sure we're not rewriting onto it
        if len(self.children) != 0:
            for child in self.children:
                child.generate(branches-1)
        else: 
            #Go straight to bottom of tree
            for move in self.board.genlegalmoves(self.turn):
                #Create child
                tboard=copy.deepcopy(self.board)
                tboard.makemove(move)
                newNode = Node(board=tboard, lastmove=move)
                
                #Continue only if game is not over
                if not self.board.over:
                    newNode.generate(branches-1)
                    #Add fully built node to children
                    self.children.append(newNode)
    def minimax(self, branches):
        if branches <= 0: return #End at 0 branches, instead of going down the tree to the final branch
        if len(self.children) == 0: return #End at bottom of tree
        ##RANDOM MOVE IS PREFERABLE AT TIE
        randomchild = random.choice(self.children)
        self.value = randomchild.value
        self.bestmove = copy.deepcopy(randomchild.lastmove)
        
        
        #SEARCH CHILDREN FOR BETTER MOVE
        for child in self.children:
            child.minimax(branches-1) # Go down the tree
            if self.turn == 1:
                if child.value > self.value: #Maximize for X
                    self.value = child.value
                    self.bestmove = copy.deepcopy(child.lastmove)
            if self.turn == -1:
                if child.value < self.value: #Minimize for O
                    self.value = child.value
                    self.bestmove = copy.deepcopy(child.lastmove)
    def sort(self):
        random.shuffle(self.children) #Add some randomness
        for i in range(0,len(self.children)):
            for x in range(0,i):
                if self.turn == 1:
                    if (self.children[i].value) > (self.children[x].value):
                        self.children[i],self.children[x] = self.children[x],self.children[i]
                if self.turn == -1:
                    if (self.children[i].value) < (self.children[x].value):
                        self.children[i],self.children[x] = self.children[x],self.children[i]
    def alphabeta(self,total,turns=3,branches=3):
        if total <= 0:
            return
        self.generate(turns)
        self.minimax(turns)
        self.sort()
        for child in self.children[:branches]:
            child.alphabeta(total-1,turns,branches)
        return self.bestmove
    def prune(self,branches):
        self.children = self.children[:branches]
    def __unicode__(self):
        s = ""
        s += (self.board.__unicode__()) + "\n"
        s += "Value:" + unicode(self.value) + "\n"
        s += "Children: " + unicode(len(self.children)) + "\n"
        s += "Turn: " + unicode(self.turn) + "\n"
        s += "Last Move: " + unicode(self.lastmove) + "\n"
        s += "Best Move: " + unicode(self.bestmove)
        return unicode(s)
    
    def childofmove(self, move):
        for child in self.children:
            if child.lastmove == move:
                return child
        return None
        