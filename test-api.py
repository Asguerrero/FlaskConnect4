# This example shows you how to use the requests package to send test queries to an HTTP API.

import requests
from textwrap import wrap

api_command = 'newgame'
api_input = 'X'
response = requests.get('http://localhost:5555/'+ api_command +'/' + api_input)


jsonResponse = response.json()
gameID = jsonResponse['ID']

# List of opponent moves that will appear as X when the board is printed. 
opponentMoves = [1, 3, 4, 3, 1, 6, 5, 7]

for move in opponentMoves:
    nextMoveResponse = requests.get('http://localhost:5555/'+ 'nextmove' +'/' + str(gameID) + '/' + str(move)+ '/' + '------------')
    nextMoveJsonResponse = nextMoveResponse.json()
    print(nextMoveJsonResponse)
    #Print board row by row 
    board = nextMoveJsonResponse['state'][0]
    boardRows = [(board[i:i+7]) for i in range(0, len(board), 7)]
    boardRows.reverse()
    for row in boardRows:
        print(row)
    
   
