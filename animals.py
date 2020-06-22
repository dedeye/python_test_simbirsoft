from flask import Flask, send_file, abort
from PIL import Image, ImageFilter
from io import BytesIO
from pathlib import Path
import requests
import uuid



def create_app():
    #create path to store images
    Path("img").mkdir(parents=True, exist_ok=True)
    
    return Flask(__name__)
    
app = create_app()


def get_url(animal):
    urls = {
        'cat': lambda: requests.get("http://aws.random.cat/meow").json()['file'],
        'dog': lambda: requests.get("http://shibe.online/api/shibes?count=1").json()[0],
        'fox': lambda: requests.get("https://randomfox.ca/floof/").json()['image'],
    }
    if animal in urls :
        return urls[animal]()
    else:
        return ""
    

uuid_generate = lambda: uuid.uuid4()

def get_image(url):
    r = requests.get(url)
    image = Image.open(BytesIO(r.content)).convert('RGB')
    (w,h) = (1024, round(image.height * (1024/image.width)))
    image = image.resize((w,h))
    return image

def filter_image(image):
    # image = image.filter(ImageFilter.CONTOUR)
    image = image.filter(ImageFilter.SMOOTH_MORE)
    return image


@app.route('/')
def hello_world():
    return 'Hello world!'


@app.route('/animal/<animal_type>')
def getAnimal(animal_type):
    url = get_url(animal_type)
    if url == "":
        abort(404)
    
    image = get_image(url)
    image = filter_image(image)

    filename = "img/" + str(uuid_generate()) + ".png"

    image.save(filename)

    return send_file(filename, mimetype='image/png')



@app.route('/history/')
def history():
    return 'under construction'

@app.route('/history/static/<uuid>')
def history_(uuid):
    return 'under construction'

    