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
    currPlayer = allBoards[gameID][1]
    targetIndex = opponentMove - 1
    while targetIndex < 42:
        if board[targetIndex] == "-":
            board[targetIndex] = currPlayer
            return board
        else:
            targetIndex += 7
    return False
    
#AI moves their piece to the next available spot, iterating through the board from left to right
def makeNextMove(gameID, board):
    previousPlayer =  allBoards[gameID][1]
    if previousPlayer == "X":
        currPlayer = "O"
    else:
        currPlayer = "X"
    index = 0
    while index < 42:
        if board[index] == "-":
            board[index] = currPlayer
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
    nextPlayer = allBoards[gameID][1]

    #Update global variable allBoards
    allBoards[gameID][0] = ''.join(currBoard)
    allBoards[gameID][1] = nextPlayer
    state = allBoards[gameID][0] + "#" + nextPlayer
    response = { 'ID': gameID, 'col': nextMove, 'state' : state}

    return json.dumps(response)


if __name__ == '__main__':
    host = 'localhost'
    port = 5555
    app.run(host=host, port=port, debug=True)