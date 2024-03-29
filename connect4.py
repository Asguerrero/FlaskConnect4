'''Connect 4 API implementation: Alex Wcislo, Carlos Flores, Valentina Guerrero'''

import flask
import json
import time

app = flask.Flask(__name__)

allBoards = {}

def updateAllBoards(opponentMove, gameID):
    print("Boards in update")
    print(allBoards)
    currState = allBoards[gameID]
    board = currState[0]
    currPlayer = currState[1]
    if currPlayer == "X":
        previousPlayer = "O"
    else:
        previousPlayer = "X"
    targetIndex = opponentMove
    while targetIndex < 42:
        if board[targetIndex] == "-":
            board[targetIndex] == previousPlayer
            break 
        else:
            targetIndex += 7

def pickNextMove(gameID):
    board = allBoards[gameID][0]
    currPlayer =  allBoards[gameID][1]
    index = 0
    while index < 42:
        if board[index] == "-":
            board[index] == currPlayer
            if (index + 1) % 7 == 0:
                return 7
            else:
                return (index+1)%7
        else:
            index += 1

def updatePlayer(gameID):
    currPlayer =  allBoards[gameID][1]
    if currPlayer == "X":
        nextPlayer = "O"
    else:
        nextPlayer = "X"
    return nextPlayer

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
    if gameID not in allBoards:
        response = {"Error": "gameID not Found"}
    # Update our local records of the board 
    # Choose next move 
    # Update state of the board with our new move
    updateAllBoards(oppCol, gameID)
    nextMove = pickNextMove()
    updatePlayer(gameID)
    response = { 'ID': gameID, 'col': nextMove, 'state' : allBoards[gameID]}

    return json.dumps(response)


if __name__ == '__main__':
    host = 'localhost'
    port = 5555
    app.run(host=host, port=port, debug=True)