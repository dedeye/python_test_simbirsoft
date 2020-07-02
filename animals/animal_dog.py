from animals.common import get_uuid, get_filename_from_uuid
from flask import Blueprint, current_app, send_file
from animals.image_processing import image_process
import requests


animal_dog = Blueprint('animal_dog', __name__)


def get_dog_raw_image():
    dog_url = "http://shibe.online/api/shibes?count=1"
    dog_image_url = requests.get(dog_url, timeout=3).json()[0]
    return requests.get(dog_image_url).content


@animal_dog.route('/animal/dog')
def dog():
    raw_image = get_dog_raw_image()

    processed_image = image_process(raw_image)

    uuid = get_uuid()

    filename = get_filename_from_uuid(uuid)
    processed_image.save(filename)

    db = current_app.config["history.db"]
    db.store_event("dog", uuid)

    return send_file(filename, mimetype='image/png')
