from animals.common import get_uuid, get_filename_from_uuid
from flask import Blueprint, current_app, send_file
from animals.image_processing import image_process
import requests

animal_fox = Blueprint('animal_fox', __name__)


def get_fox_raw_image():
    fox_url = "https://randomfox.ca/floof/"
    image_url = requests.get(fox_url, timeout=3).json()['image']
    return requests.get(image_url, timeout=3).content


@animal_fox.route('/animal/fox')
def fox():
    raw_image = get_fox_raw_image()

    processed_image = image_process(raw_image)

    uuid = get_uuid()

    filename = get_filename_from_uuid(uuid)
    processed_image.save(filename)

    db = current_app.config["history.db"]
    db.store_event("fox", uuid)

    return send_file(filename, mimetype='image/png')
