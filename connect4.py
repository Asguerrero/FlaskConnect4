import flask
import json

app = flask.Flask(__name__)

@app.route('/newgame/player')
def newgame ():
    

if __name__ == '__main__':
    app.run(debug=True)