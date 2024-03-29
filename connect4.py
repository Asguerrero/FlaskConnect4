'''Connect 4 API implementation: Alex Wcislo, Carlos Flores, Valentina Guerrero'''

import flask
import json
import time

app = flask.Flask(__name__)

allBoards = {}

def addLastMove(opponentMove, gameID, board):
    print("Boards in update", allBoards)
    currPlayer = allBoards[gameID][1]
    # if currPlayer == "X":
    #    previousPlayer = "O"
    # else:
    #    previousPlayer = "X"
    targetIndex = opponentMove - 1
    print("FIRST TARGET INDEX")
    print(board[targetIndex])
    while targetIndex < 42:
        if board[targetIndex] == "-":
            board[targetIndex] = currPlayer
            print("updateAllBoards in addLastMove", board) 
            return board
           
        else:
            targetIndex += 7

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
                return 7
            else:
                return (index+1)%7, board
        else:
            index += 1

# def defineNextPlayer(gameID):
#     currPlayer =  allBoards[gameID][1]
#     if currPlayer == "X":
#         nextPlayer = "O"
#     else:
#         nextPlayer = "X"
#     return nextPlayer

@app.route('/newgame/<player>')
def newgame (player):
    gameId = int(time.time())
    state = ["------------------------------------------", player]
    allBoards[gameId] = state
    response = {'ID' : gameId}
    print("Boards")
    print(allBoards)
    return json.dumps(response)

@app.route('/nextmove/<gameID>/<oppCol>/<state>')
def nextmove(gameID, oppCol, state):
    gameID = int(gameID)
    oppCol = int(oppCol)
    board = list(allBoards[gameID][0])
    if gameID not in allBoards:
        response = {"Error": "gameID not Found"}
    updatedBoard = addLastMove(oppCol, gameID, board)
    nextMove, currBoard = makeNextMove(gameID, updatedBoard)
    nextPlayer = allBoards[gameID][1]

    allBoards[gameID][0] = ''.join(currBoard)
    allBoards[gameID][1] = nextPlayer

    response = { 'ID': gameID, 'col': nextMove, 'state' : allBoards[gameID]}

    return json.dumps(response)


if __name__ == '__main__':
    host = 'localhost'
    port = 5555
    app.run(host=host, port=port, debug=True)