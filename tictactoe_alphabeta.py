import random

#This variable is responisble for keeping the track of the game
game_board=['-']*9

#this variable is used to keep track of moves
evalution_board=[[0,0,0],[0,0,0],[0,0,0]]

#Alpha and Beta variables for crucial for alpha and Beta prunning
alpha=-10000
#-100000 is equivalent to negative infinity
beta=10000
#100000 is equivalent to positive infinity

#this function print the game's situation
def printGameBoard(game_board):
    print(f"{game_board[0]} | {game_board[1]} | {game_board[2]} ")
    print("  +   +   ")
    print(f"{game_board[3]} | {game_board[4]} | {game_board[5]} ")
    print("  +   +   ")
    print(f"{game_board[6]} | {game_board[7]} | {game_board[8]} ")



#This function adds player move in evalution board
def insertEvalutionBoardPlayer(game_board,position):
    position_chart = {0: [0, 0], 1: [0, 1], 2: [0, 2],
                      3: [1, 0], 4: [1, 1], 5: [1, 2],
                      6: [2, 0], 7: [2, 1], 8: [2,2]}

    x=position_chart[position][0]
    y=position_chart[position][1]
    #Its a call to add move accoriding to given crediationals by player
    # 1 represents player and -1 represents computer
    moveEvalutionBoard(game_board,x,y,1)



#This function is helper for game board ,it checks if position in game board is available or not
def isEmpty(game_board,position):
  if(game_board[position]=='-'):
    return True
  else:
    False

#This function search available or free position in evalution board
def emptySpaces(evalution_board):
     empty_spaces=[]
     for i,row in enumerate(evalution_board):
         for j,col in enumerate(row):
             if evalution_board[i][j] == 0:
                 empty_spaces.append([i, j])
     return empty_spaces


#Check if board is full or not (evalution_board)
def noBoardSpaceAvailable(evalution_board):
     test_board=emptySpaces(evalution_board)
     if (len(test_board)==0):
         return True
     else:
      return False

#This function add move to the evalution board accoriding to crediationals provided in parameter
def moveEvalutionBoard(evalution_board, x, y, player):
    evalution_board[x][y] = player


#This function deal with player move on both evalution board and game board
def moveBoardPlayer(game_board,evalution_board):
    check=True
    while check:
        numbers=['0','1','2','3','4','5','6','7','8']
        position_string=input("Enter number 0-8  ")
        if(position_string in numbers and isEmpty(game_board,int(position_string))):
          position=int(position_string)
          game_board[position]='P'
          insertEvalutionBoardPlayer(evalution_board,position)
          check=False
        else:
         print("Incorrect move")



#this is a helper function which helps to insert computer(AI) in to game board
def insertComputerMoveDisplayBoard(moves):
    if(moves[0]==0):
        if(moves[1]==0):
            return 0
        elif(moves[1]==1):
            return 1
        else:
            return 2
    elif(moves[0]==1):
        if(moves[1]==0):
            return 3
        elif(moves[1]==1):
            return 4
        else:
            return 5
    else:
        if(moves[1]==0):
            return 6
        elif(moves[2]==1):
            return 7
        else:
            return 8

#This function check game winning condition met or not
def winner(evalution_board, player):
    wining_conditions= [[evalution_board[0][0], evalution_board[0][1], evalution_board[0][2]],
                  [evalution_board[0][0], evalution_board[1][0], evalution_board[2][0]],
                  [evalution_board[0][0], evalution_board[1][1], evalution_board[2][2]],
                   [evalution_board[0][1], evalution_board[1][1], evalution_board[2][1]],
                  [evalution_board[0][2], evalution_board[1][2], evalution_board[2][2]],
                  [evalution_board[0][2], evalution_board[1][1], evalution_board[2][0]],
                  [evalution_board[1][0], evalution_board[1][1], evalution_board[1][2]],
                  [evalution_board[2][0], evalution_board[2][1], evalution_board[2][2]]]

    if ([player, player, player] in wining_conditions):
        return True

    else:
        return False

#These function determine who is the winner of the game.
def gameWinner(evalution_board):
    if(winner(evalution_board,1)):
        return True
    elif(winner(evalution_board,-1)):
        return True
    else:
        False

def gameScore(evalution_board):
    if(winner(evalution_board,1)):
        return 1
    elif(winner(evalution_board,-1)):
        return -1
    else:
        return 0


#alpha beta pruning algorithm (this algorthm choses AI moves)
def alphaBetaAlgorithm(evalution_board, depth, alpha, beta, player):
    row = None
    col = None
    #depth checks how many moves are available ,if depth ==0 then no moves are available
    if (depth == 0 or gameWinner(evalution_board)):
        return [row, col, gameScore(evalution_board)]

    else:
        for space in emptySpaces(evalution_board):
            moveEvalutionBoard(evalution_board, space[0], space[1], player)
            score = alphaBetaAlgorithm(evalution_board, depth - 1, alpha, beta, -player)
            if player == 1:
                if (score[2] > alpha):
                    alpha = score[2]
                    row = space[0]
                    col = space[1]

            else:
                if (score[2] < beta):
                    beta = score[2]
                    row = space[0]
                    col = space[1]

            moveEvalutionBoard(evalution_board, space[0], space[1], 0)

            if (alpha >= beta):
                break

        if player == 1:
            return [row, col, alpha]

        else:
            return [row, col, beta]



#This function runs player move
def playerMove(game_board,evalution_board):
    moveBoardPlayer(game_board,evalution_board)

#This function runs AI moves
def computerMove(game_board,evalution_board):
    moves=alphaBetaAlgorithm(evalution_board,len(emptySpaces(evalution_board)),alpha,beta,-1)
    game_board[insertComputerMoveDisplayBoard(moves)]='C'
    moveEvalutionBoard(evalution_board,moves[0],moves[1],-1)

#This function iniate game
def startGame():

    #Player choice to take first move
    choice_check=True
    print(f"Do yo want to take first move or not ? \n ")
    while choice_check:
     choice=input("Press Y or N \t")
     if(choice=='Y' or choice=='y'):
         choice_check=False
     elif(choice=='N' or choice=='n'):
         choice_check=False
         move_choices=[0,1,2]
         x=random.choice(move_choices)
         y=random.choice(move_choices)
         moves=[x,y]
         moveEvalutionBoard(evalution_board,moves[0],moves[1],-1)
         game_board[insertComputerMoveDisplayBoard(moves)] = 'C'
     else:
         print("Wrong button\n")


    check=True
    while check:
     if(noBoardSpaceAvailable(evalution_board)==False):
        printGameBoard(game_board)
        playerMove(game_board,evalution_board)
        if(gameScore(evalution_board)==1):
          printGameBoard(game_board)
          print("Human won\n")
          check=False
          break

        if(noBoardSpaceAvailable(evalution_board)==True):
            check=False
            printGameBoard(game_board)
            print("No one won")
            break

        computerMove(game_board,evalution_board)
        if(gameScore(evalution_board)==-1):
          printGameBoard(game_board)
          print("Bot won ,Now we will take the world HAHAHAHAHA\n")
          check=False
          break
     else:
         check=False
         printGameBoard(game_board)
         print("No one won")
         break










startGame()
        









