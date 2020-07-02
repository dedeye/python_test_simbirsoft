from animals.common import get_uuid, get_filename_from_uuid
from flask import Blueprint, current_app, send_file, abort
from animals.image_processing import image_process
import requests


animal_dog = Blueprint('animal_dog', __name__)


def get_dog_raw_image():
    timeout = current_app.config["APP_REQUESTS_TIMEOUT"]

    dog_url = "http://shibe.online/api/shibes?count=1"
    dog_image_url = requests.get(dog_url, timeout=timeout).json()[0]
    return requests.get(dog_image_url, timeout=timeout).content


def save_event(uuid):
    db = current_app.config["history.db"]
    db.store_event("dog", uuid)


@animal_dog.route('/animal/dog')
def dog():
    try:
        raw_image = get_dog_raw_image()
        processed_image = image_process(raw_image)

    except Exception:
        abort(500)

    uuid = get_uuid()

    filename = get_filename_from_uuid(uuid)
    processed_image.save(filename)

    save_event(uuid)

    return send_file(filename, mimetype='image/png')
