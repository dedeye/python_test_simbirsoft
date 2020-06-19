from flask import Flask, send_file
from PIL import Image, ImageFilter
from io import BytesIO
from pathlib import Path
import requests
import uuid

app = Flask(__name__)

@app.route('/')
def helloWorld():
    return 'Hello world!'


@app.route('/animal/cat')
def getAnimalCat():
    url_req = requests.get("http://aws.random.cat/meow")
    image_req = requests.get(url_req.json()['file'])
    image = Image.open(BytesIO(image_req.content)).convert('RGB')
    image = image.filter(ImageFilter.CONTOUR).filter(ImageFilter.SMOOTH)
    name = uuid.uuid4()

    Path("img").mkdir(parents=True, exist_ok=True)

    filename = "img/" + str(name) + ".png"

    image.save(filename)


    return send_file(filename, mimetype='image/png')

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

    