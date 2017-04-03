import board, node, AI, copy


def main():
    gameboard = board.BaseBoard()
    userinput = raw_input("Would you like to be WHITE or BLACK: ")
    while userinput.upper() != "WHITE" and userinput.upper() != "BLACK":
        userinput = raw_input("Would you like to be white or black: ")
    if userinput.upper() == "WHITE":
        user = 1
    if userinput.upper() == "BLACK":
        user = -1
    
    #Get difficulty
    userinput = int(raw_input("What difficulty would you like: 1, 2, 3? "))
    if userinput == 1:
        dif = 2
    elif userinput == 2:
        dif = 3
    else:
        dif = 5
    ai = AI.AI(dif, board=copy.deepcopy(gameboard))
    while not gameboard.over:
        print(gameboard.__unicode__())
        if gameboard.turn == user: #User's turn
            row = input("Please enter a row: ")
            column = input("Please enter a column: ")
            row1 = input("Please enter a new row: ")
            column1 = input("Please enter a new column: ")
            usermove = board.Move(row, column,row1,column1)
            if gameboard.legalmove(usermove):
                gameboard.makemove(usermove)
                ai.makemove(usermove)
        else: #Computer turn
            print("AI is thinking...")
            ai.bestmove()
            aimove = ai.bestmove()
            print("AI makes move.")
            print(aimove)
            print(ai.gameTree.__unicode__())
            gameboard.makemove(aimove)
            ai.makemove(aimove)
    print("Good Game!")
    print(gameboard.__unicode__())
            
            


a = main()