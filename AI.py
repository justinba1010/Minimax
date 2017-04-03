import node, board
import random

class AI():
    def __init__(self,difficulty, board = board.BaseBoard(), turn = 1):
        self.gameTree = node.Node(board,turn)
        self.difficulty = difficulty
        self.bestmove(1)
    def bestmove(self, difficulty = None):
        difficulty = self.difficulty if difficulty == None else difficulty
        self.gameTree.generate(difficulty)
        self.gameTree.minimax(difficulty)
        
        ######No idea why this fixes it, but it does
        self.gameTree.minimax(difficulty)
        return self.gameTree.bestmove
    def alphabeta(self,difficulty = None,turns = 3, branches = 3):
        difficulty = self.difficulty if difficulty == None else difficulty
        return self.gameTree.alphabeta(difficulty, turns, branches)
    def makemove(self,move):
        if self.gameTree.childofmove(move) == None:
            self.gameTree = node.Node(board=self.gameTree.board,turn=self.gameTree.turn)
            self.gameTree.generate(1)
            if self.gameTree.childofmove(move) == None:
                return -1
        self.gameTree = self.gameTree.childofmove(move)