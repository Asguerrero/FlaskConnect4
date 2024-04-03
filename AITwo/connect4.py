# This is a very simple progrm to test that the Flask and JSON packages are correctly installed
# Ashok Khare, Oliver Tullio, Zev Goldhaber-Gordon

import flask
import json
import random
from multiprocessing import Value

counter = Value('i', 0)
app = flask.Flask(__name__)

def generate_state(col, gamestate, player):
    tempstate = gamestate
    for slot in range(35+col, col-1, -7):
        state = tempstate
        if state[slot] == '-':
            state_as_list = list(state)
            state_as_list[slot] = player
            state = ''.join(state_as_list)
            newstate = [slot, state]
            return newstate
    return None

def row_win(col, slot, state, player):
    # checking for potential sequences of 4 in a row which don't run past the limits of the board
    # if there's a possible sequence, check if the 4-in-a-row actually exists
    for i in range(-3, 1):
        if (col + i >=0 and col + i + 3 <= 6):
            if (state[slot + i] == state[slot + i + 1] == state[slot + i + 2] == state[slot + i + 3] == player):
                return True
    return False

def col_win(slot, state, player):
    # checking whether any slots run past the bottom of the board
    if (slot + 21 <= 41):
        if (state[slot] == state[slot + 7] == state[slot + 14] == state[slot + 21] == player):
            return True
    return False

def diag_win(slot, state, player):
    (left, right) = (6, 8)
    for direction in (left, right):
        for i in range(4):
            if slot + direction*(i - 3) >= 0 and slot + direction*i<= 41 and (state[slot + direction*(i-3)] == state[slot + direction*(i-2)] == state[slot + direction*(i-1)] == state[slot + direction*(i)] == player):
                return True
    return False

def win_condition(col, slot, state, player):
    if (row_win(col, slot, state, player) or col_win(slot, state, player) or diag_win(slot, state, player)):
        return True
    else:
        return False

def find_next_move(gamestate):
    player = gamestate[0]
    board = gamestate[1:]
    move = [None, None]

    for col in range(7):
        state = generate_state(col, board, player)
        if state != None:
            slot = state[0]
            boardstate = state[1]
            if (win_condition(col, slot, boardstate, player)):
                if player == "X":
                    boardstate = "O" + boardstate
                else:
                    boardstate = "X" + boardstate
                return [col, boardstate]
            else:
                move[0] = col
                move[1] = boardstate

    if move[1] != None:
        if player == "X":
            move[1] = "O" + move[1]
        else:
            move[1] = "X" + move[1]

    return move

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/newgame/<player>")
def newgame(player):
    out_json = {}
    with counter.get_lock():
        counter.value += 1
        out_json['ID'] = counter.value
    return json.dumps(out_json)

@app.route('/nextmove/<gameID>/<oppCol>/<state>')
def nextmove(gameID, oppCol, state):
    move = find_next_move(state)
    out_json = {}
    out_json['ID'] = gameID
    out_json['col'] = move[0]
    out_json['state'] = move[1]
    return json.dumps(out_json)

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    app.run(host=host, port=port, debug=True)