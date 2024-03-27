'''Connect 4 API implementation: Alex Wcislo, Carlos Flores, Valentina Guerrero'''

import flask
import json
import time

app = flask.Flask(__name__)

allBoards = {}
- - - - - - -
- - - - - - -
- - - - - - -
- - - - - - -
- - - - - - -
- - - - - - -
@app.route('/newgame/<player>')
def newgame (player):
    gameId = int(time.time())
    state = ["------------------------------------------", player]
    allBoards[gameId] = state
    response = {'ID: ': gameId}
    print(allBoards)
    return json.dumps(response)

@app.route('nextmove/<gameID>/<oppCol>/<state>')
def nextmove(gameID, oppCol, state):
    # Update our local records of the board 
    # Choose next move 
    # Update state of the board with our new move
    updateAllBoards()
    pickNextMove()

    # Return { 'ID': gameID 'col': myCol 'state' : new_gamestate }
  
if __name__ == '__main__':
    host = 'localhost'
    port = 5555
    app.run(host=host, port=port, debug=True)