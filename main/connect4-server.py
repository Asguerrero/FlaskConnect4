from flask import Flask
from flask import render_template
from _thread import *
import random
import json
import requests
import time
import threading
import sys
import urllib

# IMPORTANT: Change these Host Names and Ports as needed
# This should be the Ports (and host names) where the AI players are listening
ai_one_url = "http://aione:5000"
ai_two_url = "http://aitwo:5000"

max_gamenum = 1
state_dict = {}
ai_url_dict = {}

state_lock = threading.Lock()
ai_url_lock = threading.Lock()

app = Flask(__name__)

# This function returns the empty board state for the start of the game
def blank_state():
    state = "X#"
    for i in range(42):
        state = state + "-"
    return state

# Takes a Board which is a string of 42 characters
#  Interprets this Board as a grid of 6 rows and 7 columns
#  Returns the character in a particular row and column
def charAt(board, row, col):
    index = col + row*7
    return board[index]

# Checks for a vertical win where the top-most piece is at row,col
def isWinDown(board,row, col):
    if row > 2:
        return False
    if charAt(board, row, col) != '-':
        if charAt(board, row, col) == charAt(board, row+1, col):
            if charAt(board, row, col) == charAt(board, row+2, col):
                if charAt(board, row, col) == charAt(board, row+3, col):
                    return True
    return False

# Checks for a Diagonal win where the Top Left Piece in the Win is at row,col
def isWinDownRight(board,row, col):
    if row > 2:
        return False
    if col > 3:
        return False
    if charAt(board, row, col) != '-':
        if charAt(board, row, col) == charAt(board, row+1, col+1):
            if charAt(board, row, col) == charAt(board, row+2, col+2):
                if charAt(board, row, col) == charAt(board, row+3, col+3):
                    return True
    return False

# Checks for a Diagonal win where the Top Right Piece in the Win is at row,col
def isWinDownLeft(board,row, col):
    if row > 2:
        return False
    if col < 3:
        return False
    if charAt(board, row, col) != '-':
        if charAt(board, row, col) == charAt(board, row+1, col-1):
            if charAt(board, row, col) == charAt(board, row+2, col-2):
                if charAt(board, row, col) == charAt(board, row+3, col-3):
                    return True
    return False

# Checks for a Horizontal win where the Left-most piece is at row, col
def isWinRight(board,row, col):
    if col > 3:
        return False
    if charAt(board, row, col) != '-':
        if charAt(board, row, col) == charAt(board, row, col+1):
            if charAt(board, row, col) == charAt(board, row, col+2):
                if charAt(board, row, col) == charAt(board, row, col+3):
                    return True
    return False


# Returns True if the game has ended
def isGameOver(state):
    board = state[2:]
    sys.stderr.write(board)

    # If the board has no empty squares the game is over
    if not ('-' in board):
        return True

    for row in range(6):
        for col in range(7):
            if isWinDown(board,row,col):
                return True
            if isWinRight(board,row,col):
                return True
            if isWinDownRight(board,row,col):
                return True
            if isWinDownLeft(board,row,col):
                return True
    
    return False

# This function is intended to be used inside a thread
#  ... This function plays through a game of Connect 4 between two AI players
def play_game(num):
    global state_dict
    global ai_url_dict

    ai_urls = ai_url_dict[num]

    ####
    # Start the game
    ids = {}
    ai_answer = requests.get(ai_urls['X'] + '/newgame/X').json()
    ids['X'] = str(ai_answer['ID'])
    ai_answer = requests.get(ai_urls['O'] + '/newgame/O').json()
    ids['O'] = str(ai_answer['ID'])
    
    cur_state = blank_state()
    state_lock.acquire()
    state_dict[num] = cur_state
    state_lock.release()

    player = 'X'
    col = '0'
    ai_urls = ai_url_dict[num]

    ####
    # Repeatedly Ask the AI players for their moves
    while not isGameOver(cur_state):

        #The hash symbol in the state needs to be replaced by the code %23
        url_state = urllib.parse.quote(cur_state)
        query_url = ai_urls[player] + '/nextmove/' + ids[player] + '/' + col + '/' + url_state

        #Debug write to stderr to see output in the terminal window
        #sys.stderr.write(query_url)
        
        ai_answer = requests.get(query_url).json()
        cur_state = ai_answer['state']
        col = str( ai_answer['col'] )

        if player == 'X':
            player = 'O'
        else:
            player = 'X'
        
        state_lock.acquire()
        state_dict[num] = cur_state
        state_lock.release()

        num_seconds = random.randint(1,4)
        time.sleep(num_seconds)

    return True

@app.route('/')
def homepage():
    return render_template("homepage.html")


#Returns the state of the Game with the given Game Number
@app.route('/gamestate/<num>')
def gamestate(num):
    global state_dict
    
    state_lock.acquire()
    if(num in state_dict):
        state = state_dict[num]
    else:
        state = blank_state()
    state_lock.release()

    my_dict = {}
    my_dict['number'] = num
    my_dict['state'] = state

    return json.dumps(my_dict)


#Starts a game between the two AI players
@app.route('/watchgame')
def watchgame():

    #Select an unused game number
    global max_gamenum
    game_number = max_gamenum
    max_gamenum += 1

    players = {}
    #Randomly decide which AI is X and which is O
    if random.randint(0,1) == 0:
        players['X'] = ai_one_url
        players['O'] = ai_two_url
    else:
        players['O'] = ai_one_url
        players['X'] = ai_two_url
    ai_url_dict[str(game_number)] = players
    
    #Create a new thread to run the game
    start_new_thread(play_game, (str(game_number), ))
    
    return render_template("watchgame.html", GameNum=game_number)


if __name__ == '__main__':
    my_port = 5000
    app.run(host='0.0.0.0', port = my_port) 
