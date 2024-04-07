'''Connect 4 API implementation: Alex Wcislo, Carlos Flores, Valentina Guerrero'''

import flask
import json
import time

app = flask.Flask(__name__)

#Dictionary of all current games(gameIDs are keys) and boards(list of board string and the next player is the value)
#Our boards are build left to right, upwards. Meaning the bottom left of a connect 4 board is represented by the first character in the board string, and the top right is the last character. 
allBoards = {}

#Update the board in allBoards with the last move from the opponent. Return false if not possible (index out of range)
def addLastMove(opponentMove, gameID, board):
    if opponentMove == 0:
        return board

    player = allBoards[gameID][1]
    if player == "X":
        opponent = "O"
    else:
        opponent = "X"

    targetIndex = opponentMove - 1
    while targetIndex < 42:
        if board[targetIndex] == "-":
            board[targetIndex] = opponent
            return board
        else:
            targetIndex += 7
    return False
    
#AI moves their piece to the next available spot, iterating through the board from left to right
def makeNextMove(gameID, board):
    player =  allBoards[gameID][1]
   
    index = 0
    while index < 42:
        if board[index] == "-":
            board[index] = player
            if (index + 1) % 7 == 0:
                return 7, board
            else:
                return (index+1)%7, board
        else:
            index += 1

#Initiates a new connect 4 game with the player being X or O
@app.route('/newgame/<player>')
def newgame (player):
    gameId = int(time.time())
    state = ["------------------------------------------", player]
    allBoards[gameId] = state
    response = {'ID' : gameId}
    return json.dumps(response)

@app.route('/nextmove/<gameID>/<oppCol>/<state>')
def nextmove(gameID, oppCol, state):
    gameID = int(gameID)
    oppCol = int(oppCol)
    board = list(allBoards[gameID][0])
    
    if gameID not in allBoards:
        response = {"Error": "gameID not Found"}
        return json.dumps(response)
    
    updatedBoard = addLastMove(oppCol, gameID, board)

    if updatedBoard == False:
        response = {"Error": "Board is not valid"}
        return json.dumps(response)

    nextMove, currBoard = makeNextMove(gameID, updatedBoard)

    #Update global variable allBoards
    allBoards[gameID][0] = ''.join(currBoard) #store as a string

    # Convert board into string  Split into six rows and join them as a string
    boardRows = [(allBoards[gameID][0][i:i+7]) for i in range(0, len(allBoards[gameID][0]), 7)]
    boardRows.reverse()
    boardRows = ''.join(boardRows)

    
    player = allBoards[gameID][1]
    if player == "X":
        opponent = "O"
    else:
        opponent = "X"

    state = opponent + "#" + boardRows
    response = { 'ID': gameID, 'col': nextMove, 'state' : state}

    return json.dumps(response)


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    app.run(host=host, port=port, debug=True)