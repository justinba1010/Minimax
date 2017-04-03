import board, node, AI, copy

def main():
    filename = "log"+raw_input("name and # try ") + ".txt"
    gameboard = board.BaseBoard()
    userinput = raw_input("Would you like to be WHITE or BLACK: ")
    while userinput.upper() != "WHITE" and userinput.upper() != "BLACK":
        userinput = raw_input("Would you like to be WHITE or BLACK: ")
    if userinput.upper() == "WHITE":
        user = 1
    if userinput.upper() == "BLACK":
        user = -1
    
    #Get difficulty
    userinput = int(raw_input("What difficulty would you like: 1, 2, 3? "))
    if userinput == 1:
        dif = 1
    elif userinput == 2:
        dif = 2
    else:
        dif = 3
    ai = AI.AI(dif, board=copy.deepcopy(gameboard))
    while not gameboard.over:
        file = open(filename,"a")
        print(gameboard.__unicode__())
        if gameboard.turn == user: #User's turn
            try: #Cause oh well I'm lazy
                row = int(raw_input("Please enter a row: "))
                column = int(raw_input("Please enter a column: "))
                newrow = int(raw_input(("Please enter a new row: ")))
                newcolumn = int(raw_input(("Please enter a new column: ")))
                usermove = board.Move(row, column, newrow, newcolumn)
                if gameboard.legalmove(usermove):
                    gameboard.makemove(usermove)
                    ai.makemove(usermove)
            except:
                print("Try again.")
        else: #Computer turn
            print("AI is thinking...")
            aimove = ai.alphabeta(dif)
            print("AI makes move.")
            print(aimove)
            gameboard.makemove(aimove)
            ai.makemove(aimove)
        file.write(ai.gameTree.__unicode__().encode("UTF-8"))
        file.close()
    print("Good Game!")
    print(gameboard)
    return None



main()