# This example shows you how to use the requests package to send test queries to an HTTP API.

import requests

#Change to the command that you want to test
api_command = 'newgame'

#Change to the input you want to test
api_input = 'X'

#Make sure to use the same port that you used in your flask API
response = requests.get('http://localhost:5555/'+ api_command +'/' + api_input)


jsonResponse = response.json()
gameID = jsonResponse['ID']

nextMoveResponse = requests.get('http://localhost:5555/'+ 'nextmove' +'/' + str(gameID) + '/1/' + '------------')

nextMoveJsonResponse = nextMoveResponse.json()
print(nextMoveJsonResponse)
