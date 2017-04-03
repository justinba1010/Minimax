# Minimax
Simple Minimax AI For Senior Year

This simple AI consists of a Node class, AI class, and Board class.
The Node class handles all the minimax search, pruning, and can run any Board class that meets the requirements of:
	a winner function, that returns the score with +inf as the upper bound for player 1(WHITE), and -inf as the upper bound for player 2(BLACK).
	an isover function, tells the AI that there are no more legal moves
	a legalmove function, asks the board if a move is legal on the board
	a makemove function, tells the board to make a move and update
	a genlegalmoves function, asks for a list of legal moves for the AI to cycle through
	a __unicode__ function, that outputs the 
	a move class inside the Board file
	
