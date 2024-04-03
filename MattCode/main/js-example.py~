from flask import Flask
from flask import render_template
import random;
import json;

app = Flask(__name__)

value_dict = {}

@app.route('/')
def welcome():
    message = "Welcome to My Example Webpage."
    message = message + " This text was produced by concatenating strings in Python!"
    return render_template("homepage.html", someText = message)

#This fetches a number associated with a name
@app.route('/lookup/<name>')
def lookup_number(name):

    #If the name has been requested previously, return the stored number
    if name in value_dict:
        answer = value_dict[name]

    #If this is a brand new name, associate it with a new random number
    else:
        answer = random.randint(0,100)
        value_dict[name] = answer

    json_answer = {
        "origin": "fetch_number",
        "name":  name,
        "value":  answer
        }

    #json.dumps creates a json object
    return json.dumps(json_answer)
    

if __name__ == '__main__':
    my_port = 5121
    app.run(host='0.0.0.0', port = my_port) 
