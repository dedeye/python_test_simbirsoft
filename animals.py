from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def helloWorld():
    return 'Hello world!'


@app.route('/animal/cat')
def getAnimalCat():
    r = requests.get("http://aws.random.cat/meow")
    return r.json()['file']

@app.route('/animal/dog')
def getAnimalDog():
    return 'this is dog \"(ᓄ ᴥ ᓇ)\\'

@app.route('/animal/fox')
def getAnimalFox():
    return 'this is fox 🦊'

@app.route('/history/')
def history():
    return 'under construction'

@app.route('/history/static/<uuid>')
def history_(uuid):
    return 'under construction'

    