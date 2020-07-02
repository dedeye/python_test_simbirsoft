from animals.common import get_uuid, get_filename_from_uuid
from flask import Blueprint, current_app, send_file
from animals.image_processing import image_process
import requests


animal_cat = Blueprint('animal_cat', __name__)


def get_cat_raw_image():
    # cat_url = "http://aws.random.cat/meow"
    # return requests.get(cat_url, timeout=timeout).json()['file']
    return requests.get("https://cataas.com/cat", timeout=3).content


@animal_cat.route('/animal/cat')
def cat():
    raw_image = get_cat_raw_image()

    processed_image = image_process(raw_image)

    uuid = get_uuid()

    filename = get_filename_from_uuid(uuid)
    processed_image.save(filename)

    db = current_app.config["history.db"]
    db.store_event("cat", uuid)

    return send_file(filename, mimetype='image/png')
